# What is being tested
- Inputs, outputs and errors are compared with the school's solution
- Valgrind is also used

# How to understand errors
- Each test case corresponds to a different .csv file that's tested, and the file's name should
  indicate what's wrong in case of invalid input files. The output of failed tests will be
   mismatches between your output and the output of the school solution(a diff)

# Requirements

- A HUJI system is guaranteed to work
- A x64 Debian based Linux distribution with `python3.7` or higher, along with the `pytest` library
  might work too, but I haven't tested it.
  
  **Windows isn't supported**
  
- Compiled executable is assumed to live in the `cmake-build-debug` folder of your root project,
  and the executable is called `FractalDrawer`

# Installation

1. Clone this repository into a 'tests' directory within your project's root folder,
   this can be done via the command 
   `git clone https://github.cs.huji.ac.il/danielkerbel/test_cpp_ex2 tests`
   
   (This may ask you for your [CSE user credentials](https://wiki.cs.huji.ac.il/wiki/Password_and_OTP#OTP_and_UNIX_passwords))

2. Set a 'pytest' run configuration in PyCharm/CLion for the tester:
  `Run | Edit Configurations | + | Python tests | pytest`
  
  Under **Target**, select the **Module Name** option, and write `tester` in the text-box below
  
3. If using CLion, you might want to set a python interpreter as well by going to 
   `File | Settings | Build, Execution, Deployment | Python Interpreter` and changing from `<No
    Interpreter>` to `Python 3.7` (or higher). This isn't necessary in PyCharm.
    
    * Note: I don't recommend using CLion for running the tests, as it doesn't format errors as
      good as PyCharm.(PyCharm can display a `<Click to see differences>` link that will open
      a nice graphical diff tool)
  
# Running

1. Firstly, compile your `FractalDrawer` executable using CLion/terminal(at the `cmake-build-debug` folder)

2. Run the python tester via one of the following ways:
   - Graphically, by doing `Run | Run... | pytest for tester`
   - Via terminal, by doing `python3 PROJECT_ROOT/tests/tester.py`
   