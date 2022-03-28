# ros启动时设置默认dns

1. system->Scripts->Scripts选项卡->+，Name填写script-startup-setdns，勾选Don't Require Permissions，Source处填写

    ```routeros
    :global dnscheck false
    /log info message="dns first set to 223.5.5.5!";
    /ip dns set servers 223.5.5.5,119.29.29.29;
    /ip dns cache flush
    ```

2. 添加计划任务：system->Scheduler->+，name填写schedule-startup-setdns，Start Time选择startup，Interval填00:00:00，On Event处填写
```:execute script="script-startup-setdns"```
