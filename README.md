# pidmanager
Python module for managing PID files

## Usage:

### Create a PID object
<name> = PID_MANAGER(name='<pidfilename>', path='</path/to/pidfile>')

### Create a PID file:
<name>.create()
  
### Remove a PID file:
<name>.remove()

## Why:
I needed somethign to fill this need, and I wanted one that was smart enough to deleve an old pidfile without a matching PID. I didn't quickly find something simple and straightforward, so I wrote one. It's not on github because I think it's the best, but mostly here because I manage my own projects with git and github and figure maybe someone might want to use it or improve it.

## Anything Else?
Why yes, glad you asked. Please send a pull request if you improve this. I'm sharing it with you, please to me the courtesy of alowing me to include your improvements into my repo.
