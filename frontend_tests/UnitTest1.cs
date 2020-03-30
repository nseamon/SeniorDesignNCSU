using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.Threading;

namespace frontend_tests
{
    [TestFixture]
    public class Tests
    {
        IWebDriver driver;

        [OneTimeSetUp]
        public void Setup()
        {
            var options = new ChromeOptions();
            options.AddArgument("--window-size=1600,900");
            options.AddArgument("headless");
            driver = new ChromeDriver(options);
        }

        [Test, Order(1)]
        public void TestCreateValidAccount()
        {
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newUsername")).SendKeys("jimmy.zhang.2020");
            driver.FindElement(By.Name("newEmail")).SendKeys("jimmy.zhang@email.com");
            driver.FindElement(By.Name("verification")).SendKeys("SeniorDesignS2020");
            driver.FindElement(By.Name("newPassword")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("password-repeat")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("signup")).Click();
            // wait until success message appears
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement response = driver.FindElement(By.Id("register"));
            Assert.AreEqual("User was added successfully", response.Text);
        }

        [Test, Order(2)]
        public void TestCreateInvalidAccount() {
            // Test empty request body
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement empty = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Missing request body", empty.Text);
            
            // Test missing email
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newUsername")).SendKeys("jimmy.zhang.2020");
            driver.FindElement(By.Name("verification")).SendKeys("SeniorDesignS2020");
            driver.FindElement(By.Name("newPassword")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("password-repeat")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement noEmail = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Missing parameter email", noEmail.Text);

            // Test missing username
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newEmail")).SendKeys("jimmy.zhang@email.com");
            driver.FindElement(By.Name("verification")).SendKeys("SeniorDesignS2020");
            driver.FindElement(By.Name("newPassword")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("password-repeat")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement noUsername = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Missing parameter username", noUsername.Text);

            // Test missing password
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newUsername")).SendKeys("jimmy.zhang.2020");
            driver.FindElement(By.Name("newEmail")).SendKeys("jimmy.zhang@email.com");
            driver.FindElement(By.Name("verification")).SendKeys("SeniorDesignS2020");
            driver.FindElement(By.Name("password-repeat")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement noPw = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Missing parameter password", noPw.Text);

            // Test invalid secret code
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newUsername")).SendKeys("jimmy.zhang.2020");
            driver.FindElement(By.Name("newEmail")).SendKeys("jimmy.zhang@email.com");
            driver.FindElement(By.Name("verification")).SendKeys("secretcode");
            driver.FindElement(By.Name("newPassword")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("password-repeat")).SendKeys("seniordesign2020pw");
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement badCode = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Wrong secret_code", badCode.Text);

            // Test user already registered
            driver.Url = "http://localhost:4200/login";
            driver.FindElement(By.Name("newUsername")).SendKeys("jimmy.zhang.2020");
            driver.FindElement(By.Name("newEmail")).SendKeys("jimmy@email.com");
            driver.FindElement(By.Name("verification")).SendKeys("SeniorDesignS2020");
            driver.FindElement(By.Name("newPassword")).SendKeys("coolnewpw2020");
            driver.FindElement(By.Name("password-repeat")).SendKeys("coolnewpw2020");
            driver.FindElement(By.Name("signup")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement response = driver.FindElement(By.Id("register"));
            Assert.AreEqual("Username already registered", response.Text);
        }

        [Test, Order(3)]
        public void TestValidLogin() {
            driver.Url = "http://localhost:4200/login";
            IWebElement username = driver.FindElement(By.Name("username"));
            IWebElement password = driver.FindElement(By.Name("password"));
            // Enter valid credentials
            username.SendKeys("jimmy.zhang.2020");
            password.SendKeys("seniordesign2020pw");
            driver.FindElement(By.Id("login")).Click();
            driver.Navigate().GoToUrl("http://localhost:4200/input");
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            // At this point, user should be at input page
            // Compare heading because URL wouldn't work
            IWebElement heading = driver.FindElement(By.Id("heading"));
            Assert.AreEqual("Raw Input for Testing", heading.Text);
        }

        [Test, Order(4)]
        public void TestInvalidLogin() {
            // test invalid username
            driver.Url = "http://localhost:4200/login";
            IWebElement username = driver.FindElement(By.Name("username"));
            IWebElement password = driver.FindElement(By.Name("password"));
            username.SendKeys("Charles.Pan");
            password.SendKeys("seniordesign2020pw");
            driver.FindElement(By.Id("login")).Click();
            IWebElement errorMsg = driver.FindElement(By.Id("loginError"));
            Assert.AreEqual("Username not found in system", errorMsg.Text);

            // test invalid password
            driver.Url = "http://localhost:4200/login";
            username = driver.FindElement(By.Name("username"));
            password = driver.FindElement(By.Name("password"));
            username.SendKeys("jimmy.zhang.2020");
            password.SendKeys("invalidpw");
            driver.FindElement(By.Id("login")).Click();
            // At this point, user should be at home page
            errorMsg = driver.FindElement(By.Id("loginError"));
            Assert.AreEqual("User password incorrect", errorMsg.Text);
        }

        //[Test, Order(5)]
        public void TestLogout() {
            // Login first
            TestValidLogin();
            // Find the logout button and click it
            driver.FindElement(By.Id("loginLink")).Click();
            // Test to see we are on the login page
            Assert.AreEqual("http://localhost:4200/login", driver.Url);
        }

        [Test, Order(6)]
        public void TestValidInput()
        {
            // Login
            driver.Url = "http://localhost:4200/login";
            IWebElement username = driver.FindElement(By.Name("username"));
            IWebElement password = driver.FindElement(By.Name("password"));
            // Enter valid credentials
            username.SendKeys("jimmy.zhang.2020");
            password.SendKeys("seniordesign2020pw");
            driver.FindElement(By.Id("login")).Click();
            // Wait until textbody is present
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            // Test #1
            IWebElement textBody = driver.FindElement(By.Name("message"));
            textBody.SendKeys("{\"raw_text\": \"I will hate Merck. They suck :(\", \"time\": \"2020-05-03 12:48:30\"," 
                + "\"source\": \"TWITTER\",\"lat\": \"-26.012\",\"lon\": \"28.123\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            // Wait until success message appears
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement success = driver.FindElement(By.Name("success"));
            Assert.AreEqual("Data is submitted", success.Text);
            // Navigate to home
            driver.FindElement(By.Id("homeLink")).Click();
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement author = driver.FindElement(By.Id("author"));
            IWebElement time = driver.FindElement(By.Id("time"));
            IWebElement text = driver.FindElement(By.Id("text"));
            IWebElement source = driver.FindElement(By.Id("source"));
            Assert.AreEqual("John Steele", author.Text);
            Assert.AreEqual("2020-05-03 12:48:30", time.Text);
            Assert.AreEqual("I will hate Merck. They suck :(", text.Text);
            Assert.AreEqual("TWITTER", source.Text);
        }

        [Test, Order(7)]
        public void TestInvalidInput() {
            // Login
            driver.Url = "http://localhost:4200/login";
            IWebElement username = driver.FindElement(By.Name("username"));
            IWebElement password = driver.FindElement(By.Name("password"));
            // Enter valid credentials
            username.SendKeys("jimmy.zhang.2020");
            password.SendKeys("seniordesign2020pw");
            driver.FindElement(By.Id("login")).Click();
            // Wait until textbody is present
            driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
            IWebElement textBody = driver.FindElement(By.Name("message"));
            
            // test empty request body
            driver.FindElement(By.Name("submit")).Click();
            IWebElement error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Missing request body", error.Text);

            // test missing text
            textBody.SendKeys("{\"time\": \"2020-05-03 12:48:30\"," 
                + "\"source\": \"TWITTER\",\"lat\": \"-26.012\",\"lon\": \"28.123\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            // artifically block until a new error message is shown due to slow processing times
            while (error.Text == "Missing request body") { }
            error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Missing parameter raw_text", error.Text);

            // test invalid source
            textBody.Clear();
            textBody.SendKeys("{\"raw_text\": \"Merck is the worst company in the world they are so bad\", \"time\": \"2020-05-03 12:48:30\"," 
                + "\"source\": \"FACEBOOK\",\"lat\": \"-26.012\",\"lon\": \"28.123\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            // block
            while (error.Text == "Missing parameter raw_text") { }
            error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Invalid source", error.Text);

            // test invalid lat
            textBody.Clear();
            textBody.SendKeys("{\"raw_text\": \"Merck is the worst company in the world they are so bad\", \"time\": \"2020-05-03 12:48:30\"," 
                + "\"source\": \"TWITTER\",\"lat\": \"-90.1\",\"lon\": \"28.123\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            while (error.Text == "Invalid source") { }
            error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Latitude must be between -90 and 90", error.Text);

            // test invalid lon
            textBody.Clear();
            textBody.SendKeys("{\"raw_text\": \"Merck is the worst company in the world they are so bad\", \"time\": \"2020-05-03 12:48:30\"," 
                + "\"source\": \"TWITTER\",\"lat\": \"-26.012\",\"lon\": \"180.1\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            while (error.Text == "Latitude must be between -90 and 90") { }
            error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Longitude must be between -180 and 180", error.Text);

            // test invalid time
            textBody.Clear();
            textBody.SendKeys("{\"raw_text\": \"Merck is the worst company in the world they are so bad\", \"time\": \"2021-05-03 25:48:30\"," 
                + "\"source\": \"TWITTER\",\"lat\": \"-26.012\",\"lon\": \"28.123\",\"author\":\"John Steele\"}");
            driver.FindElement(By.Name("submit")).Click();
            while (error.Text == "Longitude must be between -180 and 180") { }
            error = driver.FindElement(By.Name("error"));
            Assert.AreEqual("Invalid time format, must be YYYY-DD-MM HH:MM:SS", error.Text);
        }

        public void TestViewEntry() {
            // NOT YET IMPLEMENTED
        }
        
        [OneTimeTearDown]
        public void Close()
        {
            driver.Close();
        }
    }
}