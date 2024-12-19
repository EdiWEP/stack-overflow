import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sovf.models import Question, Answer, AnswerComment, Vote, AnswerVote


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        usernames = ['andrei', 'bianca', 'carina', 'david', 'evelina']
        users = []
        for username in usernames:
            user = User.objects.create_user(username=username, password='password123')
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users"))

        questions_data = [
            ("What is the difference between Python lists and tuples?",
             "I want to understand why tuples are immutable in Python.",
             [
                 "Tuples are immutable, meaning their contents can't be changed after creation, which makes them hashable and suitable as keys in dictionaries.",
                 "Lists are mutable and can be modified, so they're better for use cases where data changes are needed."
             ]),
            ("How does the Java Virtual Machine (JVM) work?",
             "Can someone explain the JVM architecture in simple terms?",
             [
                 "The JVM interprets bytecode generated by the Java compiler and executes it. This makes Java platform-independent.",
                 "It provides memory management via garbage collection and ensures runtime safety by checking bytecode before execution."
             ]),
            ("What is the difference between stack and heap memory in C++?",
             "When should I use stack vs heap memory in my programs?",
             [
                 "Stack memory is automatically managed and faster, but it's limited in size. It's best for local variables.",
                 "Heap memory is larger and manually managed, ideal for dynamic memory allocation when data size is unpredictable."
             ]),
            ("What is functional programming?",
             "I keep hearing about functional programming. How does it differ from object-oriented programming?",
             [
                 "Functional programming focuses on pure functions and immutability, avoiding side effects.",
                 "Object-oriented programming organizes code into objects and uses inheritance and polymorphism."
             ]),
            ("How does DNS work?",
             "I don't understand how domain names are translated into IP addresses.",
             [
                 "DNS resolves domain names to IP addresses using a hierarchical system of name servers.",
                 "Your computer queries a DNS server, starting with a root server, then a TLD server, and finally the authoritative server."
             ]),
            ("What is an operating system kernel?",
             "What role does the kernel play in managing hardware and software resources?",
             [
                 "The kernel is the core of the OS, managing system resources like CPU, memory, and I/O devices.",
                 "It provides an interface between hardware and software, enabling applications to use hardware without direct access."
             ]),
            ("How do HTTPS and SSL/TLS ensure secure web communication?",
             "Can someone explain how encryption works in web security?",
             [
                 "HTTPS uses SSL/TLS to encrypt data between the client and server, preventing interception by attackers.",
                 "TLS provides authentication (verifying the server) and ensures data integrity by detecting tampering."
             ]),
            ("What are the principles of RESTful API design?",
             "I want to create a REST API for my project. What are the best practices?",
             [
                 "RESTful APIs follow principles like statelessness, resource-based URLs, and consistent use of HTTP methods.",
                 "Use proper status codes and JSON for responses to ensure clarity and standardization."
             ]),
            ("How does garbage collection work in Python?",
             "Can someone explain the mechanism behind Python's garbage collector?",
             [
                 "Python uses reference counting and a cyclic garbage collector to free memory occupied by unreachable objects.",
                 "The garbage collector periodically identifies and collects objects that are no longer in use."
             ]),
            ("What is the purpose of a mutex in multithreading?",
             "Why do we need mutexes, and how do they work?",
             [
                 "A mutex ensures that only one thread accesses a shared resource at a time, preventing data races.",
                 "Threads acquire the mutex before accessing the resource and release it after, ensuring thread safety."
             ]),
            ("How does the event loop work in JavaScript?",
             "Can someone explain how JavaScript handles asynchronous operations?",
             [
                 "The event loop processes tasks in the call stack and handles asynchronous operations using the task queue.",
                 "Callbacks, promises, and async/await make it possible to execute non-blocking code efficiently."
             ]),
            ("What is the difference between TCP and UDP?",
             "When should I choose TCP over UDP for networking?",
             [
                 "TCP is reliable and ensures data arrives in order, ideal for applications like web browsing and email.",
                 "UDP is faster but doesn't guarantee delivery, making it suitable for real-time applications like video streaming."
             ]),
            ("What are the common design patterns in software development?",
             "What are some useful design patterns, and when should I use them?",
             [
                 "The Singleton pattern ensures a single instance of a class, often used for logging.",
                 "The Observer pattern notifies subscribers of changes, ideal for event-driven programming."
             ]),
            ("How does virtual memory work?",
             "What are the advantages of using virtual memory in modern operating systems?",
             [
                 "Virtual memory allows the OS to use disk space as extra RAM, enabling larger programs to run.",
                 "It provides memory isolation between processes and simplifies memory management for applications."
             ]),
            ("What is the difference between shallow copy and deep copy in Python?",
             "Can someone explain how Python handles object copying?",
             [
                 "A shallow copy creates a new object but references the original's elements, which can lead to unintended side effects.",
                 "A deep copy creates a completely independent object, duplicating all nested elements."
             ]),
            ("How do relational databases store data?",
             "I want to know how relational databases organize and manage data.",
             [
                 "Relational databases store data in tables with rows and columns, linked by relationships.",
                 "Indexes are used to speed up queries, and primary/foreign keys ensure data integrity."
             ]),
            ("What is the difference between synchronous and asynchronous programming?",
             "Can someone explain the key differences with examples?",
             [
                 "Synchronous programming executes tasks sequentially, blocking until each is complete.",
                 "Asynchronous programming executes tasks concurrently, improving responsiveness by not waiting for slow operations."
             ]),
            ("How does a compiler optimize code?",
             "What are some common optimizations performed by compilers like GCC?",
             [
                 "Compilers optimize code by removing redundant instructions and improving memory usage.",
                 "Techniques like loop unrolling, inlining functions, and constant folding enhance performance."
             ]),
            ("How do content delivery networks (CDNs) improve website performance?",
             "What role does a CDN play in delivering web content?",
             [
                 "CDNs cache content on servers closer to users, reducing latency and load times.",
                 "They also balance traffic and provide redundancy, improving reliability and scalability."
             ]),
            ("What is the difference between machine code and bytecode?",
             "How does machine code differ from bytecode, and why is bytecode used?",
             [
                 "Machine code is executed directly by the CPU, while bytecode is an intermediate format interpreted by a virtual machine.",
                 "Bytecode enables portability across platforms, as it abstracts hardware differences."
             ])
        ]

        questions = []
        answers = []
        for title, content, answers_data in questions_data:
            question = Question.objects.create(
                title=title,
                content=content,
                author=random.choice(users),
            )
            questions.append(question)

            for answer_content in answers_data:
                answer = Answer.objects.create(
                    content=answer_content,
                    question=question,
                    author=random.choice(users),
                )
                answers.append(answer)

        self.stdout.write(self.style.SUCCESS(f"Created {len(questions)} questions, each with 2 answers"))

        for _ in range(100):
            if random.choice([False, True]):
                question = random.choice(questions)
                user = random.choice(users)

                while Vote.objects.filter(question=question, user=user).exists():
                    question = random.choice(questions)
                    user = random.choice(users)

                Vote.objects.create(
                    user=user,
                    question=question,
                    value=random.choice([1, 1, 1, -1]),
                )
            else:
                answer = random.choice(answers)
                user = random.choice(users)

                while AnswerVote.objects.filter(answer=answer, user=user).exists():
                    answer = random.choice(answers)
                    user = random.choice(users)


                AnswerVote.objects.create(
                    user=user,
                    answer=answer,
                    value=random.choice([1, 1, 1, -1]),
                )
        self.stdout.write(self.style.SUCCESS("Created 100 upvotes and downvotes on questions and answers"))

        comments = [
            "Thanks for sharing!",
            "This helped me understand",
            "Could you give some more details?",
            "I think OP was asking something else"
        ]
        for _ in range(10):
            answer = Answer.objects.order_by('?').first()
            AnswerComment.objects.create(
                answer=answer,
                author=random.choice(users),
                content=random.choice(comments),
            )
        self.stdout.write(self.style.SUCCESS("Created 10 answer comments"))

        self.stdout.write(self.style.SUCCESS("Done seeding"))