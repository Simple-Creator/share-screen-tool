# share-screen-tool(SST)

一、背景
= 
    目前的开源共享桌面，需配合第三方网络穿透工具，实现多人共享和接入，使用和部署不是很方便。
    开发目的是：
        1.提供独立可运行的桌面共享程序，尽量保持简单简约，方便部署和移植。
        2.交流学习

二、原理
=
                    
{sender} ->  【服务端 |SenderThreadServer| -> |Redis| -> |ReceiverThreadServer| 服务端】 -> {Receiver}

 
三、目录
= 
> share-screen-tool 主目录
>
>> 原理说明.png 
>
>> sender.py  发送接收端
>
>> receiver.py 接收客户端
>
>> screen_server_sender.py  服务端：与发送端交互
>
>> screen_server_receiver.py 服务端：与接收端交互
>


四、环境依赖
= 

1. python3
2. redis
3. 服务器一台

4. python包 : redis,opencv-python, pillow




