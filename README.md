<h1>Change</h1>

Change is an application that provides users with mature financial allocation advice. It was created for Hackrice 13, specially designed to "Reimagine banking" for Capital One. Change is meant to be a user-friendly interface that allows anyone, no matter how financially literate, to easily allocate money and save some extra change at a one-stop-shop. You can use Change by inputting in your age, salary, and how much money you will deposit for Change to allocate and watch as our algorithms determine the best way you can grow your money. In addition, try using our personal AI-powered chatbot that was designed to give tailored responses regarding the fund allocation strategy described! For this project, we used Python, PyQt5, NumPy, pandas, matplotlib, and the ChatGPT API.

<h2> How do I use Change? </h2>

To use Change, run the **PyGui.py** file and input your salary, age, deposit, and preferred risk level. When submitted, graphical results will appear on your screen. If you have any questions about your results or do not understand what you are seeing, you can use the chatbot feature by enterring the chat and asking your question.

<h3> Our Algorithm </h3>

In broad strokes, our risk algorithm takes the approach that young people should primarily invest in higher risk, long term investments, which we implement by choosing a basket of large cap tech stocks as our primary investment vehicle, with the our average return calculated using data over the past year. As people get older, they generally switch to a lower risk, shorter term investment strategy, which is represented by a higher weight towards shorter term bonds. We achieved a smooth curve for any inputted age by creating investment plans for 3 key ages, 18, 42, and 65, and linearly interpolating a continuous function between the nodes that will output a vector of weights that represent the investment plan for each age. This way, for example, a 25 year old will have a plan mathematically suited to their needs. 

We simulate the experience of a month to month use case of our banking system by generating a stochastic monthly expense component based on the average living expenses for a single person, withdrawing this amount from our cash on hand basket, and then depositing a months salary into our aforementioned allocation algorithm
