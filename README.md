HSData
======

Program in python to create a list of all the skills known by hacker schoolers.
From this list of skills, the program count the number of times each skill is mentioned per person.

Many problems arise in the cleaning of the datas. Some data are mispelled, some words/skills appear as substrings in other words/skills, some hacker schoolers wrote full sentences instead of one or two words describing their skills.
As an imperfect solution, for the words/skills included as substrings of other words/skills (like java is a substring of javascript), the program only counts if those words appear alone and not in a sentence.
For the more complicated words that do not appear as a substring, the program count those words appearing alone and also in sentences. This causes a biais.
Identifying which skills appear as substrings of other skills is only done for skills that are mentioned by at least 80 people.

The program takes care of a few typos but not all.

SkillsLargerThan80.pdf is a file created by R showing the distribution of the skills mentioned at least 80 times by hacker schoolers from the beginning of hacker school to the batch of Winter 1 2014.
