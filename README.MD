# DNSPod_ddns

这是一个利用DNSPod的动态域名解析服务的Python脚本，可以将运行本脚本的主机的IP动态更新至DNSPod的域名解析服务

本脚本利用了DNSPod API实现，API的帮助文档见 http://www.dnspod.cn/docs/records.html#dns

# 使用方式

1. Git克隆至本地

    `git clone https://github.com/senhtry/DNSPod_ddns.git`

2. 编辑ddns.conf，可配置多个域名解析至本机IP，示例

    ```
    [aa.mydomain.com]
    ID = 12345
    Token = abcdefghijklmnopqrstuvwxyzabcdef
    Format = json
    DomainID = 12345678
    RecordID = 123456789
    Domain = mydomain.com
    SubDomain = aa
    RecordLine = 默认
    ```
	
	如何获取ID、Token、DomainID、RecordID请自行搜索网上文章，有现成方案