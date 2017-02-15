import requests
import time
import datetime
import configparser


class Record:

    def __init__(self):
        self.ID = ""
        self.Token = ""
        self.Format = "json"
        self.DomainID = ""
        self.RecordID = ""
        self.Domain = ""
        self.SubDomain = ""
        self.RecordLine = "默认"
        self.Data = {}
        self.Headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
        self.NextRunTime = datetime.datetime.now()

    def __str__(self):
        print("{!s}.{!s}".format(self.SubDomain, self.Domain))

    def GetRecordIP(self):
        recordDomian = "{!s}.{!s}".format(self.SubDomain, self.Domain)
        res = requests.get("http://119.29.29.29/d", params={'dn': recordDomian}, timeout=20)
        return res.text.rstrip()

    def SetDDNS(self, localIP):
        self.Data.update(
            dict(
                login_token=("{!s},{!s}".format(self.ID, self.Token)),
                format=self.Format,
                domain_id=self.DomainID,
                record_id=self.RecordID,
                sub_domain=self.SubDomain,
                record_line=self.RecordLine,
                value=localIP,))
        try:
            curIP = self.GetRecordIP()
            if curIP:
                if curIP != localIP:
                    res = requests.post(
                        "https://dnsapi.cn/Record.Ddns", headers=self.Headers, data=self.Data, timeout=20)
                    statusCode = res.json()["status"]["code"]
                    if statusCode == "1":
                        self.PrintLog("DDNS updated to new ip: {!s}".format(localIP))
                        curIP = localIP
                        self.NextRunTime = datetime.datetime.now() + datetime.timedelta(seconds=60)
                    elif statusCode == "-2":
                        self.PrintLog("API too many record operations, blocked")
                        self.NextRunTime = datetime.datetime.now() + datetime.timedelta(hours=1)
                    else:
                        self.NextRunTime = datetime.datetime.now() + datetime.timedelta(seconds=60)
                        raise Exception("DNSPod return error status code: {!s}".format(statusCode))
                else:
                    self.PrintLog("DDNS already up-to-date: {!s}".format(localIP))
                    self.NextRunTime = datetime.datetime.now() + datetime.timedelta(seconds=60)
        except Exception as ex:
            self.PrintLog(ex)
            self.NextRunTime = datetime.datetime.now() + datetime.timedelta(seconds=60)

    def PrintLog(self, msg):
        print("Time: {!s} , Record: {!s}.{!s} : {!s}".format(
            time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()), self.SubDomain, self.Domain, msg))


def GetLocalIP():
    res = requests.get("http://v4.ipv6-test.com/api/myip.php", timeout=20)
    return res.text.rstrip()


def LoadConfig(fileName):
    config = configparser.ConfigParser()
    fileList = config.read(fileName, encoding="utf8")
    if fileList:
        print("Config file loaded: {!s}".format(fileList))
        records = []
        for section in config.sections():
            subDomain = config[section]
            record = Record()
            record.ID = subDomain.get("ID")
            record.Token = subDomain.get("Token")
            record.Format = subDomain.get("Format")
            record.DomainID = subDomain.get("DomainID")
            record.RecordID = subDomain.get("RecordID")
            record.Domain = subDomain.get("Domain")
            record.SubDomain = subDomain.get("SubDomain")
            record.RecordLine = subDomain.get("RecordLine")
            records.append(record)
            record.PrintLog("Config loaded : {!s}.{!s}".format(record.SubDomain, record.Domain))
        return records
    else:
        print("Cannot found config file")


if __name__ == "__main__":
    records = LoadConfig("ddns.conf")
    if records:
        localIP = GetLocalIP()
        while localIP:
            for record in records:
                if datetime.datetime.now() > record.NextRunTime:
                    record.SetDDNS(localIP)
            time.sleep(60)
    else:
        print("No records in config file, exit")