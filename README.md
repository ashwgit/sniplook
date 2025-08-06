# sniplook 
An utility to store and search text snippets.

A productivity tool for developers to store and search, text snippets in terminal using Python and Sqlite fts.

Note:- 
- sniplook itself does not have external dependency, bu ause the build backend it hatchling so if installations fails cause of hatchling being not found, use 

```bash
pip install hatchling
```
- While adding snippets, as sniplook waits for receiving EOF signal to understand the enf of snippets so please use Ctrl + d on linux/mac/unix and Ctrl + z on Windows.

## Installing sniplook
1. From Source 

```bash
git clone https://github.com/ashwgit/sniplook.git
cd sniplook
pip install .
```

### Usage
- Adding a text snippet 
```bash
sniplook add 
```
Then enter the text you want to save and hit Ctrl + D (i.e EOF). 
Note:- It will create a db in user home directory at the following path - ~/.sniplook/db/sqlite.db


- Searching for snippets
```bash
sniplook
```
Just type for what you want to search for and hit enter. 

#### Example 
```bash
$ sniplook add 
-
podman run hello-world 

$ sniplook
search: podman 
---
podman run hello-world

```

### How does it helps?  

1. You can add your long text snippets and search for it without leaving cli. 
    - Be it long linux commands, 
    - some scripts and functions which you can't remember but you always need it once in a while.
2. Ever feared loosing your snippets while switching your laptop? All snippets are stored in sqlite db file locally, which you can just copy to new system. 
3. It do supports Fuzzy search so your minor spelling mistakes in search query gives your proper return.

### Feature features you can expect. 
1. Tagging of your text snippets using LLM models so you can find things easily from tag if you need it.
2. Optionally using cloud database which can help finding your snippets on different machines without copying local db.

