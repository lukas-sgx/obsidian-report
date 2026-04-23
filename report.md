# OBSIDIAN REPORT
Black-box Audit
In this phase, we analyzed the binary using reverse engineering tools and manual fuzzing. List of the tools you used :
    - Cutter
    - Ghidra
    - Gdb-ged
    - Upx

#### Key discoveries:
    - The binary was found to be packed with UPX. It was successfully unpacked using upx -d `obsidian`, revealing the original executable for further static analysis


## Vulnerability Report
Below is the list of vulnerabilities discovered, ranked by severity:


Vulnerability #1: activate_emergency_protocols


Severity: Critical
Type: Harcoded Credentials
Location: function activate_emergency_protocols
Discovered in: Black-box

Description:
The emergency administration flow relies on a static password embedded directly in the binary logic.
After selecting the action activate_emergency_protocols, the code compares user input against a hardcoded literal value admin123 using strcmp.
Because the credential is fixed and reused, any attacker who discovers it once can consistently bypass authentication and trigger privileged emergency/admin functionality.
This is a direct authentication design failure: no secret rotation, no per-user credentialing, no secure secret storage, and no rate-limiting evidence in the PoC path.


Proof of Concept:
```c
iVar1 = strcmp(&var_78h, "admin123");
if (iVar1 == 0) {
    putstr("{Emergency protocols activated, you are now admin !}");
}
```

Impact:
Privilege Escalation (high-confidence)
Unauthorized access to admin/emergency controls (high-confidence)
Potential full operational takeover of critical reactor functions if this command is reachable in production context (critical business/operational risk)


Vulnerability #2: alchemy


Severity: High
Type: Hardcoded Secret / Reversible Obfuscation
Location: alchemy/decompiler/main.c, function alchemy
Discovered in: Black-box

Description:
The module constructs a sensitive value directly in memory from hardcoded integer constants.
The secret is not protected cryptographically and can be reconstructed by reversing endianness and concatenating constant fragments.
Any attacker with binary access can recover the embedded secret without authentication.

Proof of Concept:
```c
var_17h = 0x61505f6f62614c7b;
var_fh._0_4_ = 0x6f777373;
var_fh._4_2_ = 0x6472;
var_fh._6_1_ = 0x7d;
```

Impact:
Sensitive data exposure
Secret recovery by reverse engineering
Potential reuse of recovered secret in other modules


Vulnerability #3: check_cooling_pressure


Severity: High
Type: Hardcoded Credentials / Predictable Secret Disclosure
Location: check_cooling_pressure command flow (runtime output path)
Discovered in: Black-box

Description:
The command output leaks a secret value in a deterministic way that can be extracted by scripted interaction.
No dynamic secret derivation or strong access control is observed in the PoC path.

Proof of Concept:
```python
pid.sendline(b'check_cooling_pressure')
for _ in range(5):
        line = pid.recv(timeout=3.0)
print(line.decode().split("\n")[0][16:])
```

Impact:
Unauthorized disclosure of sensitive operational information
Facilitates chained attacks with other privileged functions


Vulnerability #4: run_diagnostic


Severity: High
Type: Hardcoded Credential / Debug Backdoor
Location: run_diagnostic command path
Discovered in: Black-box

Description:
The diagnostic feature accepts a static debug token to unlock privileged output.
This behavior is consistent with a hidden maintenance backdoor left in production logic.

Proof of Concept:
```python
pid.sendline(b'run_diagnostic')
pid.sendline(b'debug')
line = pid.recvlines(timeout=1.0)
```

Impact:
Privilege escalation through undocumented debug path
Information disclosure from restricted diagnostics


Vulnerability #5: check_reactor_status


Severity: Medium
Type: Weak Encryption (Caesar Cipher)
Location: check_reactor_status/decompiler/main.c, function check_reactor_status
Discovered in: Black-box

Description:
Critical reactor data is protected with a Caesar shift (gap=3), which is trivially reversible.
This is obfuscation, not encryption, and does not provide confidentiality.

Proof of Concept:
```python
line = pid.recvline_startswith(b'Encrypted message:')
print(cipher(line.decode().split()[2], 3))
```

Impact:
Loss of confidentiality of supposedly protected status data
Attackers can decode messages without key material


Vulnerability #6: send_status_report


Severity: Medium
Type: Reversible Encoding Misused as Encryption
Location: send_status_report/decrypt.sh and status report generation path
Discovered in: Black-box

Description:
Status report data is only Base64-encoded and presented as if protected.
Base64 is not a security mechanism and can be decoded instantly.

Proof of Concept:
```bash
echo "$report" | base64 -d
```

Impact:
Sensitive status report disclosure
False sense of security for transmitted or stored data


Vulnerability #7: init_steam_turbine


Severity: Medium
Type: Insecure Randomness (Predictable PRNG)
Location: external_lib/init_steam_turbine/decompiler/main.c, function main
Discovered in: Black-box

Description:
Random values are generated with rand() seeded by time(NULL).
This pattern is predictable and reproducible when seed timing is known or approximated.

Proof of Concept:
```c
srand((__u_int)time((time_t *)0x0));
printf("magix - decompil: %i\n", rand());
```

Impact:
Predictable random-dependent behavior
Potential bypass of logic that assumes randomness


Vulnerability #8: simulate_meltdown


Severity: Medium
Type: Insecure Randomness / Brute-force Trigger
Location: simulate_meltdown command path
Discovered in: Black-box

Description:
Critical branch triggering can be reached by repeatedly invoking the function until a random-dependent condition occurs.
This demonstrates non-robust control relying on weak randomness.

Proof of Concept:
```python
while True:
        pid.sendline(b'simulate_meltdown')
        line = pid.recvline_startswith("Critical Error:", timeout=1.0)
        if line != b'':
                break
```

Impact:
Unauthorized triggering of critical error states
Increased operational risk from probabilistic abuse


Vulnerability #9: read_turbine_config


Severity: High
Type: Path Traversal via Symlink (File Access Control Bypass)
Location: external_lib/read_turbine_config/decompiler/main.c, function main
Discovered in: Black-box

Description:
Input sanitization only blocks ".." but trusts files under Data/.
An attacker can create a symlink in Data/ pointing to arbitrary filesystem targets (e.g., /etc/passwd), bypassing intended directory restrictions.

Proof of Concept:
```bash
ln -s /etc/passwd Data/passwd

```

Impact:
Arbitrary file read (subject to process privileges)
Disclosure of host and credential-related data


Vulnerability #10: run_turbine


Severity: Medium
Type: Integer Signedness / Boundary Validation Flaw
Location: external_lib/run_turbine/decompiler/main.c, function main
Discovered in: Black-box

Description:
User input is parsed with atoi then stored in an unsigned integer.
Supplying negative values (e.g., -1) leads to inconsistent comparisons and unsafe control flow behavior.

Proof of Concept:
```python
pid.sendline(b'run_turbine')
pid.sendline(b'-1')
```

Impact:
Logic bypass of input constraints
Unexpected runtime behavior and potential stability issues


Vulnerability #11: turbine_explode


Severity: Medium
Type: Integer Conversion / Sentinel Boundary Abuse
Location: external_lib/turbine_explode/decompiler/main.c, function main
Discovered in: Black-box

Description:
Input is converted with strtoll and cast to int, then compared to specific sentinel values.
Supplying edge integers triggers the dangerous branch directly.

Proof of Concept:
```python
pid.sendline(b'turbine_temperature')
pid.sendline(b'2147483646')
```

Impact:
Forced critical failure path
Potential denial of service and unsafe state transitions


Vulnerability #12: set_reactor_power


Severity: Medium
Type: Runtime State Validation Bypass (Debugger-assisted)
Location: set_reactor_power runtime stack variable
Discovered in: Black-box

Description:
The PoC demonstrates bypass by modifying local state in memory at runtime.
This indicates insufficient hardening against tampering and weak trust in mutable local validation state.

Proof of Concept:
```gdb
set {int}($rbp-0x4)=0x7ffffc19
continue
```

Impact:
Bypass of expected validation constraints
Unauthorized state transitions when debugger access exists


Vulnerability #13: load_fuel_rods


Severity: Critical
Type: Buffer Overflow (Likely Stack-based)
Location: load_fuel_rods command path
Discovered in: Black-box

Description:
The PoC repeatedly triggers behavior consistent with a memory corruption primitive labeled as buffer overflow.
The command accepts attacker-controlled input and reaches abnormal output path, indicating likely stack overwrite potential.

Proof of Concept:
```python
pid.sendline(b'load_fuel_rods')
pid.sendline(b'10')
output = pid.recvrepeat(timeout=1.2)
```

Impact:
Potential code execution or control-flow corruption
Process crash / denial of service
High exploitability in native binary context


Vulnerability #14: monitor_radiation_levels


Severity: Critical
Type: Control-Flow Hijack via Stack Memory Corruption (Likely)
Location: monitor_radiation_levels runtime stack frame
Discovered in: Black-box

Description:
The exploit overwrites a stack slot with a function address and diverts execution.
This behavior is consistent with memory safety weakness enabling direct control-flow manipulation.

Proof of Concept:
```gdb
set *(long long*)($rbp-0x8)=0x004024a0
continue
```

Impact:
Arbitrary control-flow redirection
Potential code execution in process context
Severe integrity compromise


Vulnerability #15: turbine_remote_access


Severity: Medium
Type: Unsafe Temporary File Handling / Information Disclosure
Location: external_lib/turbine_remote_access/decompiler/main.c, function main
Discovered in: Black-box

Description:
The module stores sensitive access data in a temporary file under Data/ and leaves a readable window before cleanup.
An attacker monitoring the directory can read secrets before unlink.

Proof of Concept:
```bash
find ./Data/ -type f -exec cat {} \;
```

Impact:
Disclosure of sensitive access tokens/flags
Race-window based data leakage


Vulnerability #16: emergency_shutdown


Severity: High
Type: Authentication / Logic Bypass (Debugger-assisted)
Location: emergency_shutdown runtime control flow
Discovered in: Black-box

Description:
By using instruction pointer jumps and register manipulation, the PoC forces a success state without legitimate flow completion.
This reveals fragile runtime trust assumptions under tampering.

Proof of Concept:
```gdb
jump *0x004034a8
set $eax=1
continue
```

Impact:
Forced privileged shutdown flow
Bypass of expected safety checks in debug-capable context


Vulnerability #17: quit


Severity: Medium
Type: Logic Bypass (Debugger-assisted Branch Manipulation)
Location: quit runtime instruction pointer path
Discovered in: Black-box

Description:
Execution can be redirected to post-validation logic through direct jump, bypassing normal checks and flow constraints.

Proof of Concept:
```gdb
quit
jump *0x00402f69
```

Impact:
Bypass of intended quit/control checks
Potential abuse of hidden branches in debug context


Vulnerability #18: log_system_event


Severity: Medium
Type: Runtime Memory Tampering Bypass (Debugger-assisted)
Location: log_system_event runtime memory pointers
Discovered in: Black-box

Description:
The PoC modifies in-memory bytes at strategic addresses to alter behavior and access internal logs.
This demonstrates weak resilience against runtime tampering and state integrity attacks.

Proof of Concept:
```gdb
set {char}($rdi+4)=0
set {char}($rax+4)=0
continue
```

Impact:
Unauthorized access to protected log resources
Integrity loss of runtime decision state


Vulnerability #19: configure_cooling_system


Severity: High (Unverified)
Type: Potential RCE (Insufficient Evidence)
Location: configure_cooling_system
Discovered in: Black-box

Description:
The available exploit artifact claims remote code execution but does not include payload details or reproducible steps.
This finding is retained as a risk indicator pending technical validation.

Proof of Concept:
```text
run RCE
```

Impact:
Potential remote code execution if confirmed
Requires additional verification before final severity lock


Vulnerability #20: call_api


Severity: Medium
Type: Client-side Secret Exposure / Obfuscation Reversal
Location: call_api/script.js
Discovered in: Black-box

Description:
Sensitive information is recoverable by iterating an obfuscated JavaScript API call.
The protection relies on obscurity rather than access control or cryptography.

Proof of Concept:
```javascript
for (let i = 0; i < 20; i++) {
    try { console.log(i, qNNX.GNNS(i)); }
    catch(e) {}
}
```

Impact:
Exposure of embedded secret values
Loss of confidentiality for client-distributed logic/data

