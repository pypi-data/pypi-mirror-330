# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import os
import sys

from typing import List, Optional

from .functions import FunctionInfo, Registry
from .loader import load_function, install
from .logging import logger
from .otel import otel_manager, initialize_azure_monitor, configure_opentelemetry

from .bindings.context import get_context
from .bindings.meta import load_binding_registry, is_trigger_binding, from_incoming_proto, to_outgoing_param_binding, to_outgoing_proto
from .bindings.out import Out
from .utils.constants import (FUNCTION_DATA_CACHE,
                              RAW_HTTP_BODY_BYTES,
                              TYPED_DATA_COLLECTION,
                              RPC_HTTP_BODY_ONLY,
                              WORKER_STATUS,
                              RPC_HTTP_TRIGGER_METADATA_REMOVED,
                              SHARED_MEMORY_DATA_TRANSFER,
                              TRUE,
                              PYTHON_ENABLE_OPENTELEMETRY,
                              PYTHON_ENABLE_OPENTELEMETRY_DEFAULT,
                              WORKER_OPEN_TELEMETRY_ENABLED,
                              PYTHON_ENABLE_DEBUG_LOGGING)
from .utils.current import get_current_loop, execute, run_sync_func
from .utils.env_state import get_app_setting, is_envvar_true
from .utils.helpers import change_cwd, get_worker_metadata
from .utils.tracing import serialize_exception

metadata_result: Optional[List] = None
metadata_exception: Optional[Exception] = None
result = None  # Todo: type is coroutine?
_functions = Registry()
_function_data_cache_enabled: bool = False
_host: str = None
protos = None


# Protos will be the retry / binding / metadata protos object that we populate and return
async def worker_init_request(request):
    logger.info("V1 Library Worker: received worker_init_request")
    global result, _host, protos, _function_data_cache_enabled
    init_request = request.request.worker_init_request
    host_capabilities = init_request.capabilities
    _host = request.properties.get("host")
    protos = request.properties.get("protos")
    if FUNCTION_DATA_CACHE in host_capabilities:
        val = host_capabilities[FUNCTION_DATA_CACHE]
        _function_data_cache_enabled = val == TRUE

    capabilities = {
        RAW_HTTP_BODY_BYTES: TRUE,
        TYPED_DATA_COLLECTION: TRUE,
        RPC_HTTP_BODY_ONLY: TRUE,
        WORKER_STATUS: TRUE,
        RPC_HTTP_TRIGGER_METADATA_REMOVED: TRUE,
        SHARED_MEMORY_DATA_TRANSFER: TRUE,
    }
    if get_app_setting(setting=PYTHON_ENABLE_OPENTELEMETRY,
                       default_value=PYTHON_ENABLE_OPENTELEMETRY_DEFAULT):
        initialize_azure_monitor()

        if otel_manager.get_azure_monitor_available():
            capabilities[WORKER_OPEN_TELEMETRY_ENABLED] = TRUE


    # loading bindings registry and saving results to a static
    # dictionary which will be later used in the invocation request
    load_binding_registry()
    install()

    # No indexing in init for V1 functions

    return protos.WorkerInitResponse(
        capabilities=capabilities,
        worker_metadata=get_worker_metadata(protos),
        result=protos.StatusResult(status=protos.StatusResult.Success)
    )


# worker_status_request can be done in the proxy worker

async def functions_metadata_request(request):
    logger.info("V1 Library Worker: received worker_metadata_request")
    global protos
    # Setting result as None here. If this is a V1 function, nothing to return
    return protos.FunctionMetadataResponse(
                    use_default_metadata_indexing=True,
                    function_metadata_results=None,
                    result=protos.StatusResult(
                        status=protos.StatusResult.Success))


async def function_load_request(request):
    logger.info("V1 Library Worker: received worker_load_request")
    global protos
    func_request = request.request.function_load_request
    function_id = func_request.function_id
    function_metadata = func_request.metadata
    function_name = function_metadata.name
    function_app_directory = function_metadata.directory

    try:
        if not _functions.get_function(function_id):
            func = load_function(
                function_name,
                function_app_directory,
                func_request.metadata.script_file,
                func_request.metadata.entry_point)

            _functions.add_function(
                function_id, func, func_request.metadata, protos)

        return protos.FunctionLoadResponse(
                    function_id=function_id,
                    result=protos.StatusResult(
                        status=protos.StatusResult.Success))

    except Exception as ex:
        return protos.FunctionLoadResponse(
                    function_id=function_id,
                    result=protos.StatusResult(
                        status=protos.StatusResult.Failure,
                        exception=serialize_exception(ex, protos)))


async def invocation_request(request):
    logger.info("Library Worker: received worker_invocation_request")
    global protos
    invoc_request = request.request.invocation_request
    invocation_id = invoc_request.invocation_id
    function_id = invoc_request.function_id
    threadpool = request.properties.get("threadpool")

    try:
        fi: FunctionInfo = _functions.get_function(
            function_id)
        assert fi is not None

        args = {}

        for pb in invoc_request.input_data:
            pb_type_info = fi.input_types[pb.name]
            if is_trigger_binding(pb_type_info.binding_name):
                trigger_metadata = invoc_request.trigger_metadata
            else:
                trigger_metadata = None

            args[pb.name] = from_incoming_proto(
                pb_type_info.binding_name,
                pb,
                trigger_metadata=trigger_metadata)

        fi_context = get_context(invoc_request, fi.name,
                                 fi.directory)

        # Use local thread storage to store the invocation ID
        # for a customer's threads
        fi_context.thread_local_storage.invocation_id = invocation_id
        if fi.requires_context:
            args['context'] = fi_context

        if fi.output_types:
            for name in fi.output_types:
                args[name] = Out()

        if fi.is_async:
            if otel_manager.get_azure_monitor_available():
                configure_opentelemetry(fi_context)

            call_result = await execute(fi.func, **args)  # Not supporting Extensions
        else:
            _loop = get_current_loop()
            call_result = await _loop.run_in_executor(
                threadpool,
                run_sync_func,
                invocation_id, fi_context, fi.func, args)

        if call_result is not None and not fi.has_return:
            raise RuntimeError(
                f'function {fi.name!r} without a $return binding'
                'returned a non-None value')

        output_data = []
        if fi.output_types:
            for out_name, out_type_info in fi.output_types.items():
                val = args[out_name].get()
                if val is None:
                    # TODO: is the "Out" parameter optional?
                    # Can "None" be marshaled into protos.TypedData?
                    continue

                param_binding = to_outgoing_param_binding(
                    out_type_info.binding_name, val,
                    pytype=out_type_info.pytype,
                    out_name=out_name,
                    protos=protos)
                output_data.append(param_binding)

        return_value = None
        if fi.return_type is not None:
            return_value = to_outgoing_proto(
                fi.return_type.binding_name,
                call_result,
                pytype=fi.return_type.pytype,
                protos=protos
            )

        # Actively flush customer print() function to console
        sys.stdout.flush()

        return protos.InvocationResponse(
                    invocation_id=invocation_id,
                    return_value=return_value,
                    result=protos.StatusResult(
                        status=protos.StatusResult.Success),
                    output_data=output_data)

    except Exception as ex:
        return protos.InvocationResponse(
                    invocation_id=invocation_id,
                    result=protos.StatusResult(
                        status=protos.StatusResult.Failure,
                        exception=serialize_exception(ex, protos)))


async def function_environment_reload_request(request):
    """Only runs on Linux Consumption placeholder specialization.
    This is called only when placeholder mode is true. On worker restarts
    worker init request will be called directly.
    """
    logger.info("V1 Library Worker: received worker_env_reload_request")
    try:
        global protos

        func_env_reload_request = \
            request.request.function_environment_reload_request
        protos = request.properties.get("protos")

        # Append function project root to module finding sys.path
        if func_env_reload_request.function_app_directory:
            sys.path.append(func_env_reload_request.function_app_directory)

        # Clear sys.path import cache, reload all module from new sys.path
        sys.path_importer_cache.clear()

        # Reload environment variables
        os.environ.clear()
        env_vars = func_env_reload_request.environment_variables
        for var in env_vars:
            os.environ[var] = env_vars[var]

        if is_envvar_true(PYTHON_ENABLE_DEBUG_LOGGING):
            root_logger = logging.getLogger("azure.functions")
            root_logger.setLevel(logging.DEBUG)

        # calling load_binding_registry again since the
        # reload_customer_libraries call clears the registry
        load_binding_registry()
        install()

        capabilities = {}
        if get_app_setting(
                setting=PYTHON_ENABLE_OPENTELEMETRY,
                default_value=PYTHON_ENABLE_OPENTELEMETRY_DEFAULT):
            initialize_azure_monitor()

            if otel_manager.get_azure_monitor_available():
                capabilities[WORKER_OPEN_TELEMETRY_ENABLED] = (
                    TRUE)



        # Change function app directory
        if getattr(func_env_reload_request,
                   'function_app_directory', None):
            change_cwd(
                func_env_reload_request.function_app_directory)

        return protos.FunctionEnvironmentReloadResponse(
                capabilities=capabilities,
                worker_metadata=get_worker_metadata(protos),
                result=protos.StatusResult(
                    status=protos.StatusResult.Success))

    except Exception as ex:
        global metadata_exception
        metadata_exception = ex
        return protos.FunctionEnvironmentReloadResponse(
                result=protos.StatusResult(
                    status=protos.StatusResult.Failure,
                    exception=serialize_exception(ex, protos)))
