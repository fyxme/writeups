# Hacky holidays - Space Race

Hacky Holidays Space Race was on during July 2021 and we decided to participate with a few friends. I had already participated in the previous Hacky holiday which was in december 2020 and so I knew the challenges were high quality and we were bound to learn new things.

The CTF was ongoing for 4 weeks which is considered quite long for a CTF but leaves a lot more time for people attempt the challenges. There were 3 challenge release phases with each new phase starting on Friday the following week and the last phase was 10 days long.

We played in all 3 phases and managed to do quite a few of the challenges. However, CTFs are quite draining and take a lot of time so its hard to sustain for extended period of times. Most of our hacking was done the weekends after the release and we didnt have the motivation to do any challenges in the last week.

Here's all the challenges we ended up doing:
![[hacky holidays - space race.png]]

## Awesome
- The challenges were amazing and very diverse
- We really enjoyed the non standard challenges they had such as:
	- quantum challenges
		- We used one of them to have an introduction to quantum computing at work during a work CTF session
	- redteam challenges
		- Both were interesting to showcase Active Directory attacks and allowed us to practice the new PrintNightmare exploit which was released not long before the CTF.
- Great team mentality
	- People tried to push themselves and nurture their "I have no idea what to do but I'll try it anyways mentality" which I think is something that CTFs teach you which boot2root really doesn't
	- Awesome communication and collaboration trying to solve challenges together
- We deployed internal tooling to collaborate on stuff
- We wrote tools for some of the challenges which will be open-sourced when the CTF ends
- Finding unintended solutions to break certain challenges
	- The first redteam challenge was supposed to be a kerberoasting challenge however we managed to exploit the DC with PrintNightmare. Good way to practice new exploits.
	- Using bruteforce to solve the quantum snacks challenge by abusing the check website (we also did it the intended way after to learn about quantum)
	- Abusing writeable file locations to help with the Power Snacks challenges
	- "The intended way might not be the only way to solve a challenge."
- Always a fan of web challenges and these ones didn't dissapoint! Lots of great challenges showcasing various concepts.
- The design of the CTF Portal was amazing... The best I've seen in a while 

## Issues encountered
- I wiped the collaboration server by mistake the day before phase 3 started. This deleted all writeups we had made up to that point. Very demotivating... We didn't end up rewriting many of them and therefore don't have many writeups for this CTF. 

Not much to complain about... It was a really fun CTF!

### Remediations
- Setup automated daily backups of collaboration server so that we could recover data if it gets wiped again 


## Final remarks

**Congratulations Deloitte, that was an awesome CTF.** The challenges were great, diverse and required thinking out of the box which is exactly what you expect from a CTF.

Would recommend any cyber security enthousiast to participate in the next Hacky Holidays CTF. 

![[great-success.gif]]