# DNSPod_ddns

����һ������DNSPod�Ķ�̬�������������Python�ű������Խ����б��ű���������IP��̬������DNSPod��������������

���ű�������DNSPod APIʵ�֣�API�İ����ĵ��� http://www.dnspod.cn/docs/records.html#dns

# ʹ�÷�ʽ

1. Git��¡������

    `git clone https://github.com/senhtry/DNSPod_ddns.git`

2. �༭ddns.conf�������ö����������������IP��ʾ��

    ```
    [aa.mydomain.com]
    ID = 12345
    Token = abcdefghijklmnopqrstuvwxyzabcdef
    Format = json
    DomainID = 12345678
    RecordID = 123456789
    Domain = mydomain.com
    SubDomain = aa
    RecordLine = Ĭ��
    ```
	
	��λ�ȡID��Token��DomainID��RecordID�����������������£����ֳɷ���