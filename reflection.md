# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- I included the classes Owner, Pet, Task, and Scheduler. For an Owner, they are able to have a name, pets, and availability. For Owner, you can add and remove a pet, add a name, add hours they are available each day of the week. For simplicity, we'll assume their availability remains the same each week. For a Pet, it contains a name, type, and tasks. For Pet, you can add a name and what type it is (ex: cat). You can also add different types of tasks (ex: feeding) that need to be completed for the Pet. For a Task, it contains a name, status, priority, recurrence, due date, and length to complete. For Task, you can add its name (ex: feeding) along with a status of whether it's been completed or not. You can add a priority using a simple numerical scale with 1 being high priority and 10 being low priority. Multiple tasks can have the same priority ranking. A task can also have a recurrence for whether it's a 1 time task, weekly, monthly, etc. The task will also have a time to complete in minutes along with a due date of when the task must be completed by. If it's a recurring task, it must be completed as per the recurring schedule. For a Scheduler, it contains daily task lists. The Scheduler adds tasks and sorts tasks for an owner. An owner can have multiple pets and the scheduler should be able to support multiple pets within the same time frame. We'll assume tasks can be completed at the same time for multiple pets only if they are the same breed. An example of this would be if an owner has 2 dogs, both dogs can be walked at the same time. These tasks do not need to be completed at different times.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- When developing the skeleton, the first version of the skeleton code that was output by the AI added a whole bunch of attributes and functions that I never mentioned, such as medical notes and the pet's age. The AI seemed to want to complicate the ask and not use the UML as is, which I think was well intentioned but overcomplicates the task of building a pet task scheduling app. Medical notes might be great for an overall pet wellness app, but are not relevant for tasks like playing catch with the dog. I rejected these AI suggestions and requested the AI to use only the information in the UML while also ensuring no missing relationships or bottlenecks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
