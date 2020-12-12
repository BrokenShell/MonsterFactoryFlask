# Monster Factory | Flask App
By Robert Sharp


## Technical Info
- Interface: HTML, CSS, JavaScript
- Control Logic: Python, Flask
- Data Options: CSV, SQL, Postgres, MongoDB
- Toolkit: Cython [Fortuna](https://pypi.org/project/Fortuna/) 
- Core Engine: C++ [Storm](https://github.com/BrokenShell/Storm/)
- Developer: [Robert Sharp](https://www.linkedin.com/in/robert-w-sharp/)


## Developer Notes
An issue came up in the virtual environment used for the hosting of this project: 
pythonanywhere.com. Apparently the version of gcc used doesn't have full c++17 
support. To solve the issue I implemented the std::clamp function, see below. 

```cpp
template<typename T>
constexpr const T& clamp(const T& v, const T& lo, const T& hi) {
    return v < hi ? std::max(v, lo) : std::min(v, hi);
}
```

## Project Evolution
### MonsterFactory v0.0.5: More Monsters!
- Adds the ability to load older monsters via the archive.

### MonsterFactory v0.0.4: Premature Monster Summation Antidote
- Fixes a bug that caused the form to post prematurely.

### MonsterFactory v0.0.3: Monster Diversity Patch
- Adds support for latin characters.

### MonsterFactory v0.0.2
- Minimum Viable Product

### MonsterFactory v0.0.1
- Initial Planning Phase
