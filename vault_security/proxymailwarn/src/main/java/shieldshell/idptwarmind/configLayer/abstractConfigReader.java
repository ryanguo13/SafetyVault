package shieldshell.idptwarmind.configLayer;

public abstract class abstractConfigReader {

    //bro自己写构造函数，初始化得在构造里搞定！抽象类不让我写构造函数

    public abstract String[] readWebsiteInfo() throws Exception;

    public abstract String[] readMailServerInfo() throws Exception;

    public abstract String[] readReceiverInfo() throws Exception;
}
