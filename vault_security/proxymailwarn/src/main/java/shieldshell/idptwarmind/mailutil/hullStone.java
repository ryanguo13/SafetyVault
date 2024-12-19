package shieldshell.idptwarmind.mailutil;

import jakarta.mail.Authenticator;
import jakarta.mail.PasswordAuthentication;
import jakarta.mail.Session;
import jakarta.mail.Transport;
import shieldshell.idptwarmind.configLayer.yamlReader;

import java.util.Properties;

public class hullStone {
    Session mailServer;

    public hullStone(yamlReader reader) throws Exception {
        Properties props = new Properties();
        String[] mailServerInfo = reader.readSenderConfig();

        props.put("mail.smtp.host", mailServerInfo[0]);
        props.put("mail.smtp.port", mailServerInfo[1]);
        props.put("mail.smtp.auth", true);
        props.put("mail.smtp.starttls.enable", "true");

        this.mailServer = Session.getInstance(props, new Authenticator() {
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(mailServerInfo[2], mailServerInfo[3]);
            }
        });
    }

    @Deprecated
    public void senderLogin(yamlReader reader) throws Exception {

    }

    @Deprecated
    public void sendMessage(yamlReader reader, String remains) throws Exception{


        String sender = reader.readSenderConfig()[2];
        var arylistString = reader.readReceiverConfig();
        String[] receiverString = arylistString.toArray(new String[arylistString.size()]);

        var message = new mailMessage().
                getEmailInstace(this.mailServer, sender, receiverString, remains);
        Transport.send(message);
    }

    public void sendMessage(yamlReader reader, String remains, String todayUsed) throws Exception{


        String sender = reader.readSenderConfig()[2];
        var arylistString = reader.readReceiverConfig();
        String[] receiverString = arylistString.toArray(new String[arylistString.size()]);

        var message = new mailMessage().
                getEmailInstace(this.mailServer, sender, receiverString, remains);
        Transport.send(message);
    }


}
