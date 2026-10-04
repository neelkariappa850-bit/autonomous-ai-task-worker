\# Autonomous AI Task Worker



A prototype autonomous AI task worker that accepts a natural-language task, creates an execution plan, interacts with a simulated company environment, handles failures, requests approval for consequential actions, and verifies the final outcome.



\## Problem Statement



The goal of this project is to demonstrate how an AI worker can take a high-level task and autonomously execute it using computer-based tools.



Example task:



> Find the latest invoice from Acme Corp, save the payment in the internal system, and verify that it was saved.



The worker breaks this task into actions, locates the relevant invoice, extracts the required information, interacts with a simulated internal finance portal using browser automation, verifies the result, and produces an evidence-based completion report.



\---



\## Key Features



\- Natural-language task input

\- Automatic task planning

\- Dynamic company identification

\- Invoice discovery from a local repository

\- Invoice data extraction

\- Browser automation using Playwright

\- Simulated internal company portal

\- Retry mechanism for temporary failures

\- Result verification

\- Evidence collection

\- Human approval before payment submission

\- Safe cancellation when approval is denied

\- Human-readable completion report



\---



\## Architecture



```text

&#x20;                   User

&#x20;                     |

&#x20;                     v

&#x20;            Natural Language Task

&#x20;                     |

&#x20;                     v

&#x20;             Task Worker / Planner

&#x20;                     |

&#x20;         +-----------+-----------+

&#x20;         |                       |

&#x20;         v                       v

&#x20;  Invoice Repository       Task Execution

&#x20;         |                       |

&#x20;         v                       v

&#x20;  Invoice Analyzer       Playwright Browser

&#x20;                                 |

&#x20;                                 v

&#x20;                      Mock Company Portal

&#x20;                                 |

&#x20;                                 v

&#x20;                           Verification

&#x20;                                 |

&#x20;                        +--------+--------+

&#x20;                        |                 |

&#x20;                        v                 v

&#x20;                    Success            Failure

&#x20;                        |                 |

&#x20;                        |                 v

&#x20;                        |              Retry

&#x20;                        |                 |

&#x20;                        +--------<--------+

&#x20;                                 |

&#x20;                                 v

&#x20;                        Evidence Report

Project Structure



autonomous-ai-worker/

│

├── backend/

│   ├── agent/

│   │   ├── planner.py

│   │   ├── ai\_planner.py

│   │   ├── invoice\_analyzer.py

│   │   └── task\_worker.py

│   │

│   ├── tools/

│   │   ├── file\_reader.py

│   │   └── browser.py

│   │

│   └── main.py

│

├── mock\_company/

│   ├── invoices/

│   │   ├── acme\_invoice\_001.txt

│   │   ├── acme\_invoice\_002.txt

│   │   └── globex\_invoice\_001.txt

│   │

│   ├── templates/

│   │   └── index.html

│   │

│   └── app.py

│

├── tests/

│

├── .env

├── .gitignore

├── README.md

└── requirements.txt



Technologies Used

Python

FastAPI

Flask

Playwright

OpenAI API integration

HTML

JavaScript

File-based mock data

How It Works

1\. Task Input



The user enters a natural-language task.



Example:



Find the latest invoice from Globex Ltd, save the payment in the internal system, and verify that it was saved.

2\. Task Planning



The worker converts the task into executable steps:



1\. Find latest invoice

2\. Extract invoice information

3\. Save payment

4\. Verify result

3\. Company Identification



The worker identifies the requested company from the natural-language task.



For example:



Find the latest invoice from Globex Ltd



results in:



Company identified: Globex Ltd

4\. Invoice Discovery



The worker searches the invoice repository and identifies the most recent invoice based on invoice date.



5\. Data Extraction



The worker extracts:



Invoice number

Invoice date

Amount

Due date

Status

6\. Safety Check



Before submitting a payment, the worker asks for explicit user approval.



Approve this payment? (yes/no):



If the user rejects the action, the payment is not submitted.



7\. Browser Execution



After approval, Playwright opens the simulated internal company portal and enters the payment information.



8\. Failure Recovery



The worker supports bounded retries for temporary failures.



Example:



Attempt 1

Temporary failure

&#x20;       |

&#x20;       v

Retry

&#x20;       |

&#x20;       v

Attempt 2

Success

9\. Verification



The worker checks that the submitted invoice number, amount, and due date appear correctly in the portal.



The worker does not assume that a button click means the operation succeeded.



10\. Evidence



The worker produces an evidence-based completion report containing:



Invoice source

Invoice number

Amount

Due date

Number of attempts

Payment submission status

Verification status

Setup

1\. Clone the repository

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd autonomous-ai-worker

2\. Create a virtual environment

python -m venv venv

3\. Activate the environment



Windows PowerShell:



.\\venv\\Scripts\\Activate.ps1

4\. Install dependencies

pip install -r requirements.txt

5\. Install Playwright browser

python -m playwright install chromium

6\. Configure environment variables



Create a .env file:



OPENAI\_API\_KEY=your\_api\_key\_here



The API key is optional for the current deterministic prototype workflow.



Never commit the .env file to GitHub.



Running the Mock Company Portal



Start the simulated company portal:



python mock\_company\\app.py



The portal runs at:



http://127.0.0.1:5001



Keep this terminal running.



Running the Task Worker



Open another terminal, activate the virtual environment, and run:



python -m backend.agent.task\_worker



Enter a task such as:



Find the latest invoice from Acme Corp, save the payment in the internal system, and verify that it was saved.

Example Successful Result

TASK COMPLETION REPORT

============================================================



Status: VERIFIED

Invoice: AC-2026-002

Amount: INR 87500

Due Date: 2026-11-05

Attempts: 1



Evidence:

\- Invoice successfully located

\- Source: mock\_company\\invoices\\acme\_invoice\_002.txt

\- Payment submitted to internal portal

\- Payment presence verified

\- Invoice number, amount and due date matched



FINAL STATUS: TASK COMPLETED AND VERIFIED

Failure Recovery



The prototype can recover from a temporary internal portal failure.



Example:



Attempt 1

Payment verification failed.

Retrying with the same task...



Attempt 2

Payment action completed successfully.



VERIFICATION SUCCESSFUL!



The retry mechanism is bounded to avoid uncontrolled repeated actions.



Safety Behavior



The worker does not automatically submit a consequential payment.



It requests explicit approval:



Approve this payment? (yes/no):



If the user enters:



no



the worker stops before submitting the payment.



Example result:



Payment action cancelled by user.



Status: FAILED

Payment was not submitted because user approval was not provided.

Design Decisions

Narrow Scope



The prototype intentionally focuses on invoice processing rather than attempting to automate arbitrary computer tasks.



This allows the core autonomous behavior to be demonstrated reliably.



Mock Environment



No real financial systems or credentials are used.



A simulated company portal and local invoice repository provide a safe environment for demonstrating computer interaction.



Verification



The worker does not assume that an action succeeded simply because the browser clicked a button.



It checks the resulting portal state and compares the saved values with the expected invoice data.



Retry



Temporary failures are handled using a bounded retry mechanism rather than repeatedly attempting an action indefinitely.



Human-in-the-loop



Consequential actions require explicit user approval.



Evidence-based Completion



The worker returns evidence describing what it found, what action it performed, and how the final result was verified.



Limitations

The current prototype uses a simulated company environment.

Invoice files use a simple text format.

The deterministic planner supports a limited task domain.

Browser selectors are designed for the mock portal.

The current retry strategy is intentionally simple.

Production authentication, permissions, audit logging, and distributed execution are outside the prototype scope.

The external LLM planner is optional because the core prototype should remain functional without API availability.

The current system does not yet support arbitrary websites or unrestricted computer tasks.

Future Improvements

Fully LLM-driven planning

More browser and file-system tools

Better failure classification

Alternative recovery strategies

Persistent task memory

Screenshot-based visual verification

More robust authentication handling

Structured audit logs

Additional task types

Human approval interface

Dockerized deployment

Automated test suite

More sophisticated task decomposition

Demo Scenarios

Scenario 1 — Successful Execution



Task:



Find the latest invoice from Acme Corp, save the payment, and verify it.



Expected:



TASK COMPLETED AND VERIFIED

Scenario 2 — Failure and Recovery



A temporary portal failure is simulated.



Expected:



Attempt 1 → Failure

Attempt 2 → Success

Scenario 3 — Safety Rejection



When prompted:



Approve this payment? (yes/no):



Enter:



no



Expected:



Payment action cancelled by user.

Scenario 4 — Generalization



Task:



Find the latest invoice from Globex Ltd, save the payment, and verify it.



Expected:



Invoice: GL-2026-001

Amount: INR 64000

Due Date: 2026-11-10

Status: VERIFIED

Security



No real credentials, confidential company information, or unauthorized systems are used.



API keys and environment variables are excluded from version control using .gitignore.



The mock environment is designed specifically for safe demonstration.



Project Status



Prototype completed with:



Task planning

Natural-language task input

Dynamic company identification

Invoice discovery

Invoice data extraction

Browser automation

Failure detection

Bounded retry

Result verification

Evidence reporting

Human approval

Safety cancellation

Multi-company support

Simulated internal company environment

&#x20;                     

