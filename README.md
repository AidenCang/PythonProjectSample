# AWsgi
Python
Python实现WSGI，主要用于解决Python异步框架和服务之间的通信标准接口

在WSGI为同步Python应用程序提供标准的地方，ASGI为异步和同步应用程序提供了一个标准，具有WSGI向后兼容性实现以及多个服务器和应用程序框架。

`WSGI兼容性`
ASGI也被设计为WSGI的超集，并且在两者之间有一种定义的转换方式，允许WSGI应用程序通过转换包装器（在asgiref 库中提供）在ASGI服务器内运行。线程池可用于远离异步事件循环运行同步WSGI应用程序。
[AWSGI](https://asgi.readthedocs.io/en/latest/)

# Channels通道
核心类(两大类同步和异步):
1.同步类型:

    class WebsocketConsumer(SyncConsumer):
    class JsonWebsocketConsumer(WebsocketConsumer):
    
2.异步类型

    class AsyncWebsocketConsumer(AsyncConsumer):
    class AsyncJsonWebsocketConsumer(AsyncWebsocketConsumer):

[Channels](https://github.com/andrewgodwin/channels-examples)

# django-websocket-redis
[django-websocket-redis](https://github.com/jrief/django-websocket-redis)


## 异常类的使用
类路径:
venv/lib/python3.7/site-packages/channels/exceptions.py

class RequestAborted(Exception):
class RequestTimeout(RequestAborted):
class InvalidChannelLayerError(ValueError):
class AcceptConnection(Exception):
class DenyConnection(Exception):
class ChannelFull(Exception):
class MessageTooLarge(Exception):
class StopConsumer(Exception):


# Django认证系统
# Django会话系统

# websocket 开发调试工具

https://www.npmjs.com/package/wscat
http://coolaf.com:1010/tool/chattest