"""
    This module contains the HealthStatus Enum and HealthCheck class.
    The HealthStatus Enum contains the status and message of the health check.
    The function host_health_check() will simply host a health check server on port 8081.
"""
from enum import Enum


class HealthStatus(Enum):
    OkStatus = True
    OkMessage = "I'm well"
    NotOkStatus = False
    NotOkMessage = "I'm not well"
                    
                    
# class JsonHandlerWithGpu(http.server.BaseHTTPRequestHandler):
#     log_enable = False

#     def log_message(self, format: str, *args: Any) -> None:
#         if self.log_enable:
#             return super().log_message(format, *args)
    
#     def log_request(self, code: Union[int, str] = "-", size: Union[int, str] = "-") -> None:
#         if self.log_enable:
#             return super().log_request(code, size)
    
#     def do_GET(self):
#         """ Override the do_GET method to handle HealthCheck GET request """
#         try:
#             self.send_response(200)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             response = to_gpu_healthcheck_dict(status=HealthStatus.OkStatus.value, 
#                                             message=HealthStatus.OkMessage.value, 
#                                             is_cuda_available=torch.cuda.is_available(), 
#                                             gpu_count=torch.cuda.device_count())
#             self.wfile.write(json.dumps(response).encode('utf-8'))
#         except Exception as e:
#             self.send_response(500)
#             self.send_header('Content-type', 'application/json')
#             self.end_headers()
#             response = to_error_response(e)
#             self.wfile.write(json.dumps(response).encode('utf-8'))
#             print(e)
        
# def host_health_check(port: int = 8081):
#     """ The function simply hosts a health check server on port 8081. 
#         Usecase: 
        
#             - When the server is not designed to server HTTP request like: PubSub server, Celery server, etc.
#             - When you just want to check the health of the server but not the whole API framework.
            
#         How to setup: when the server is running in MultiProcess mode -> this server needs to be served in a separate thread
        
#         import threading

#         health_check_thread = threading.Thread(target=host_health_check)
        
#         health_check_thread.start()
        
#         This will start a health check server on port 8081 which is running on a separate thread.
            

#     Args:
#         port (int, optional): port hosting the GPU check client. Defaults to 8081.
#     """
#     # Create a simple HTTP server using the built-in modules
#     with socketserver.TCPServer(("", port), JsonHandlerWithGpu) as httpd:
#         print(f"--------Serving Worker Health Check on port {port}--------")
#         # Start the server with GPU 
#         httpd.serve_forever()
