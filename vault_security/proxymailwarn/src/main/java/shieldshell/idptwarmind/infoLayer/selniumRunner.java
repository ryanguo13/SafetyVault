package shieldshell.idptwarmind.infoLayer;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.edge.EdgeOptions;
import shieldshell.idptwarmind.configLayer.yamlReader;

import java.util.concurrent.TimeUnit;

public class selniumRunner {

    private yamlReader configResolver;
    public WebDriver seleniumDriver;

    public selniumRunner(yamlReader configResolver, boolean headless) {
        this.configResolver = configResolver;

        if(headless){
            var options = new EdgeOptions();
            options.addArguments("--headless", "--disable-gpu");
            this.seleniumDriver = new EdgeDriver(options);
        }else{
            this.seleniumDriver = new EdgeDriver();
        }
    }


    public void loginToAddr() throws Exception{
        seleniumDriver.get(configResolver.readAddr());
        seleniumDriver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS);


        //user name xpath://*[@id="email"]
        //user pass xpath://*[@id="password"]
        var sendUserName = this.seleniumDriver.findElement(By.xpath("//*[@id=\"email\"]"));
        sendUserName.sendKeys(configResolver.readUserName());
        var sendUserPasswrod = this.seleniumDriver.findElement(By.xpath("//*[@id=\"password\"]"));
        sendUserPasswrod.sendKeys(configResolver.readPassword());


        seleniumDriver.manage().timeouts().implicitlyWait(1, TimeUnit.SECONDS);
        //click button
        var loginButton = this.seleniumDriver.findElement(By.xpath("//*[@id=\"app\"]/section/div/div/div/div[2]/form/div/div[5]/button"));
        loginButton.click();

    }

    public String getRemainingRoams() throws Exception{
        //the Xpath to the card I WANT
        ////*[@id="app"]/div/div[3]/section/div[2]/div[2]/div/div[2]
        String pathtoRemainningRoamsCardbody = "//*[@id=\"app\"]/div/div[3]/section/div[2]/div[2]/div/div[2]";
        //if(!isElementPresent(seleniumDriver, By.xpath(pathtoRemainningRoamsCardbody))){
            //throw new Exception("Selenium Webdrive at Wrong Page");
        //}
        //懒得纠错了，就这样吧

        //this is Xpath to the changing value
        ////*[@id="app"]/div/div[3]/section/div[2]/div[2]/div/div[2]/div[2]/span
        var RemaningRoams = this.seleniumDriver.findElement(By.xpath("//*[@id=\"app\"]/div/div[3]/section/div[2]/div[2]/div/div[2]/div[2]/span"));

        return RemaningRoams.getText();
    }

    public void quitseleniumSep() {
        this.seleniumDriver.quit();
        this.seleniumDriver = null;
        this.configResolver = null;
    }
}
