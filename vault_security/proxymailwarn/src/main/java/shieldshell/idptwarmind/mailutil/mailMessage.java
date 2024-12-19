package shieldshell.idptwarmind.mailutil;

import jakarta.mail.Message;
import jakarta.mail.Session;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;

import java.util.Date;

//mail content with header, should leave place to name different people
public class mailMessage {
    MimeMessage emailInstace = null;

    public MimeMessage getEmailInstace
        (Session session, String sender, String[] receiver, String remaining)
            throws Exception {

        //this is FROM/TO part
        this.emailInstace = new MimeMessage(session);
        this.emailInstace.setFrom(new InternetAddress(sender));
        this.emailInstace.addRecipients
                (Message.RecipientType.TO, mailMessage.StrtoNetAddr(receiver));

        //this is subject and body part
        this.emailInstace.setSubject("Amalthea Outpost Assault Record");
        this.emailInstace.setSentDate(new Date());
        this.emailInstace.setText(
                "Dear User of Web3SafetyVault:\n" + "\n" +
                "Greeting. This is daily report from Amalthea Outpost. Today, the attacker trying to breakthrough are:\n" +
                remaining + "\n" +
                "Please consider take actions on these attackers. Amalthea Outpost keep defending you from attack.\n" +
                "Best,\nAmalthea Overwatch Outpost"
        );

        return this.emailInstace;
    }

    public MimeMessage getEmailInstace
            (Session session, String sender, String[] receiver, String remaining, String todayused)
            throws Exception {

        //this is FROM/TO part
        this.emailInstace = new MimeMessage(session);
        this.emailInstace.setFrom(new InternetAddress(sender));
        this.emailInstace.addRecipients
                (Message.RecipientType.TO, mailMessage.StrtoNetAddr(receiver));

        //this is subject and body part
        this.emailInstace.setSubject("Proxy Remaining Roaming");
        this.emailInstace.setSentDate(new Date());
        this.emailInstace.setText(
                "Dear Pirates of my Proxy:\n\n" +
                        "Greeting. Until today, the remaining roaming is: " +
                        remaining + "GB. " +
                        "And until now, you have used " + todayused + "GB." +
                        " Please use my roaming frugally and wisely.\n\n" +
                        "Best,\nAmalthea Overwatch Outpost"
        );

        return this.emailInstace;
    }


    private static InternetAddress[] StrtoNetAddr(String[] strAddr) throws Exception {

        InternetAddress[] NetAddr = new InternetAddress[strAddr.length];
        for (int i = 0; i < strAddr.length; i++) {
            NetAddr[i] = new InternetAddress(strAddr[i]);
        }
        return NetAddr;
    }

}
