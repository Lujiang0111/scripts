# ros每分钟自动切换dns

1. system->Scripts->Scripts选项卡->+，Name填写script-change-dns，勾选Don't Require Permissions，Source处填写

    ```routeros
    :global dnscheck
    :local curcheck ([:ping 192.168.8.3 count=5 interval=100ms]>3)
    :if ($curcheck && !$dnscheck) do={
        :log info message="dns change to 192.168.8.3!";
        :set dnscheck true;
        :ip dns set servers 192.168.8.3;
        :ip dns cache flush}
    :if (!$curcheck && $dnscheck) do={
        :log info message="dns change to 223.5.5.5!";
        :set dnscheck false;
        :ip dns set servers 223.5.5.5,119.29.29.29;
        :ip dns cache flush}
    ```

2. 添加计划任务：system->Scheduler->+，name填写schedule-change-dns，Start Time选择startup，Interval填00:01:00，On Event处填写
```:execute script="script-change-dns"```
