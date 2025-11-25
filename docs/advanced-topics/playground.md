🧪 Docker Playground
=======================

Once you have built a container image (`madlad-custom` in the example below) you can drop into an interactive session and experiment with anything that lives inside – from running a quick MadGraph job to plotting histograms on the fly – it has everything you need (including ROOT).

---

### 1️⃣ Launch the Container

```bash
# Start an interactive bash session inside the container.
#   - `--rm`  → remove the container when you exit
#   - `-it`   → keep STDIN open and allocate a TTY
#   - `-v $PDW:/root`  → mount your current working directory (or any other folder)
#   - `madlad-custom`  → the image name you built
docker run --rm -it -v $PDW:/root madlad-custom bash
```

> **Tip** – If you don’t have a `$PDW` environment variable, just replace it with the absolute path of any directory you want to expose inside the container.  
> E.g. `-v $(pwd):/root`.

Once you’re inside, the shell is just like a normal Linux terminal. The full MadLAD toolchain is already installed and ready to use.

---

### 2️⃣ “Hello, MadGraph”

```bash
mg5     # run MadGraph
```