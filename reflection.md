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

The constraints my scheduler considers are time and priority.
- I decided that these constraints mattered most, specifically time, because if the tasks are not completed within a certain period, then the pet could go hungry, get fleas, etc. so it has the biggest impact to the well being of the animals. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- One tradeoff my scheduler makes is that each the scheduler works backwards from deadlines. It places each task as late as possible while still meeting its due time. This means that tasks that could be started earlier in the day won't be started because it's optimized for being done as close to the due time as possible

- The tradeoff is reasonable in this scenario because an owner may want some breaks in between tasks and not complete all the tasks in 1 giant time block. It seems more realistic for how a person lives life vs. doing 5 hours of tasks in a row. The owner can sleep in as late as possible while guaranteeing every task finishes by its deadline.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used AI tools (Copilot + Claude) during this project to help with desing brainstorming for the UML diagram and deciding what attributes each class should have. I also used the AI to help with debugging issues with any of the AI generated code that was created.
- The prompts that were the most helpful were the ones where I gave it the exact files to look at as well as highlighting certain lines of code for the AI to focus on. This allowed it to pinpoint bugs that it could then address successfully. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- I didn't accept the AI suggestion to include a filter schedule by pet. It wanted to make a filter to know what tasks each pet was going to complete in the daily schedule. 
- I evaluated the suggestion by using the Streamlit app and trying to add some pets myself for an owner and seeing how it filtered the tasks by pet. When I tried to filter one of the pets, it deleted the entire section and nothing got filtrered. The AI tried to add something that wasn't needed and it didn't even work, so it goes to show don't always trust everything the AI outputs.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- Behaviors that I tested:
✓ Sorting correctness: tasks returned in chronological order
✓ Recurrence logic: daily task completion creates next day's task
✓ Conflict detection: overlapping incompatible tasks are flagged
✓ Parallel execution: same task for same-breed pets runs simultaneously
✓ Sequential scheduling: same task for different-breed pets avoids conflicts
- These tests are important because they ensure the scheduling system is putting the tasks in the proper order and that the tasks can actually be completed at the times it proposes. That's the key purpose behind the app. Parallel and sequential scheduling is the little bit I added that makes it a bit more complicated to schedule, so it's crucial to ensure this works correctly to also help save the owner time for tasks that can be done at the same time.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- I'm fairly confident that the scheduler works correctly for the behaviors I planned for because I have 13 tests validating the behavior along with an example script with a schedule that works. 
- The edge cases I'd test with more time are pets with the same name, repeated tasks for the same pet, and having so many tasks that a schedule is impossible to create to complete all the tasks.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I'm most satisfied with the logic of allowing same breeds with the same tasks to have overlapping tasks while not the same breeds can't overlap. I feel like this is different than what was probably intended with the app but more realistic to what real life is since if you have 2 dogs, you can walk them at the same time. You don't need to do the tasks sequentially.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- I'd focus mainly on the polish, ensuring edge cases are completely handled, and error handling. An example is that if you were to enter invalid input, like symbols or numbers for the name, it should disallow that input and ask for the user to enter a valid name. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- One important thing I learned about designing systems is that they can and will evolve over time as more complexity is introduced into the system. AI tends to make things more robust and detailed, and as such, systems designed with just a UML diagram initially are almost guaranteed to be changed by the time it is written in code.
