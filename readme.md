### Prerequisites

Create a file named `.env` with contents similar to the following:

```
ENDPOINT=10.1.1.13
USERNAME=yourusername
PASSWORD=yourpassword
```

You may also need to install the `dotenv` library, which is used to store environment variable values outside of the script.

```
pip install python-dotenv
```

### What is this and why should I care?

This script is simply an introduction on how to leverage Python when interacting with F5 BIG-IQ's APIs, including AS3. It is meant to act as an introduction to working with APIs and gaining an understanding of the basic processes associated with and surrounding **C**reate, **R**ead, **U**pdate, and **D**elete operations, generally referred to as **CRUD**.

Python's easy-to-consume syntax coupled with the Requests library provides a clean, simple platform upon which basic automation tooling can be created. This script is quite flat in nature, intentionally, and leaves room for improvement and expansion.

But you may still be asking *why should I care*?

In essentially all lines of work, there exists the consumption, or input, of data, the processing thereof, and resultant output. Technology, and the tools created as a result of technological progress, continues to displace the need for manual labor when performing the input/process/output sequence. Because of this, humans must continually adapt with ever-increasing frequency and re-tool in order to remain relevant when pursuing jobs of reasonable return.

Being able to speak the language of machines is absolutely critical in today's job markets, and understanding how to manipulate computers so they can speak with one another to achieve our goals is of extremely high value. IT infrastructure provisioning and maintenance is a huge overhead and an area which dramatically benefits from *proper* process automation.

Proper process automation begins with quality data and the tools with which to manipulate said data. It must also be wrapped with diligent governance, oversight, and business process and technical analysis. F5 BIG-IQ with AS3 provides a foundation upon which all of these concepts can be designed, driven, and matured.