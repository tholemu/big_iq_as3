### Prerequisites

Create a file named `.env` with contents similar to the following:

```
ENDPOINT=10.1.1.13
USERNAME=yourusername
PASSWORD=yourpassword
```

You may also need to install the `dotenv` library, which is used to manage environment variable values outside of the script.

```
pip install python-dotenv
```

### Usage

Ensure you've cloned this repo to the machine used to interact with your BIG-IQ instance and created the `.env` file.

Run the following command:

```
python_requests_example_workflow.py
```

The following process takes place as the script executes:

1. Juice Shop AS3 declaration is loaded and deployed
1. The deployed application is moved from BIG-IQ's default global application *Unknown Applications* to a unique global app named *Juice_Shop*
1. A modified declaration, which includes an advanced web application firewall policy, is deployed
1. A series of traffic tests are run to generate statistics within BIG-IQ
1. The Juice Shop application service and global app are deleted


### WAF Tester Installation / Setup / Usage
**Install**
```
sudo pip install git+https://github.com/aknot242/f5-waf-tester.git
```

**Setup**
```
sudo f5-waf-tester --init
```

You will be asked a series of questions. Use the following values below; for all other values, leave the default value and simply press Enter:

```
[BIG-IP] Host []: 10.1.1.4
[BIG-IP] Username []: admin
[BIG-IP] Password []: {password}
ASM Policy Name []: Juice_Shop_WAF_Policy
Virtual Server URL []: https://10.1.10.11
Blocking Regular Expression Pattern [<br>Your support ID is: (?P<id>\d+)<br>]:
Number OF Threads [25]:
[Filters] Test IDs to include (Separated by ',') []:
[Filters] Test Systems to include (Separated by ',') []:
[Filters] Test Attack Types to include (Separated by ',') []:
[Filters] Test IDs to exclude (Separated by ',') []:
[Filters] Test Systems to exclude (Separated by ',') []:
[Filters] Test Attack Types to exclude (Separated by ',') []:
```

**Run Test**
```
sudo f5-waf-tester
```

### What is this and why should I care?

This script is simply an introduction on how to leverage Python when interacting with F5 BIG-IQ's APIs, including AS3. It is meant to act as an introduction to working with APIs and gaining an understanding of the basic processes associated with and surrounding **C**reate, **R**ead, **U**pdate, and **D**elete operations, generally referred to as **CRUD**.

Python's easy-to-consume syntax coupled with the Requests library provides a clean, simple platform upon which basic automation tooling can be created. This script is quite flat in nature, intentionally, and leaves room for improvement and expansion.

But you may still be asking *why should I care*?

In essentially all lines of work, there exists the consumption, or input, of data, the processing thereof, and resultant output. Technology, and the tools created as a result of technological progress, continues to displace the need for manual labor when performing the input/process/output sequence. Because of this, humans must continually adapt with ever-increasing frequency and re-tool in order to remain relevant when pursuing jobs of reasonable return.

Being able to speak the language of machines is absolutely critical in today's job markets, and understanding how to manipulate computers so they can speak with one another to achieve our goals is of extremely high value. IT infrastructure provisioning and maintenance is a huge overhead and an area which dramatically benefits from *proper* process automation.

Proper process automation begins with quality data and the tools with which to manipulate said data. It must also be wrapped with diligent governance, oversight, and business process and technical analysis. F5 BIG-IQ with AS3 provides a foundation upon which all of these concepts can be designed, driven, and matured.