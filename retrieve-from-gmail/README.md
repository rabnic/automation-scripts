# Fetch Daily Coding Problems
The overall purpose of this script is to log into my Gmail account and retrieve all emails sent  daily by [Daily Coding Problem](https://www.dailycodingproblem.com) with subject *'Daily Coding Problem: Problem #.'*

So what is **Daily Coding Problem** all about?

> "We'll be sending you one programming interview question every day that was asked recently by top tech companies.
> Each question should take under one hour to solve, including actual working code and some test.", - Marc

## Todo tasks | The `gmail-script.py` script should:
- [x] Log into Gmail account and return Gmail API service
- [x] Fetch list of message/email ids from specified query
- [x] Fetch a certain message/email using message id
- [x] Get email subject and extract coding problem number and difficulty
- [x] Get email body and extract company name and interview question
- [x] Return list of tuples in form of (question_number, difficulty, company_name, question)
- [ ] Store the above list locally for future reference
- [ ] Refactor code to first check local and only start fetching emails where it last left of. Not fetch all redundant emails on every request.