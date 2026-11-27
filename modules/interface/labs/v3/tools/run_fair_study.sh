#!/usr/bin/env bash
# FINAL-02 model comparison on the running emulator (NOT a phone), airplane mode, ONE model per run (never two LLMs).
# Test APK only: the model goes through the protected A02 load of the app (sealed fd, SHA-256, native policy).
# Usage (from modules/): run_fair_study.sh <res dir: model.gguf + bench JSONs> <out dir> <label> <sha256> <small> <context> <threads> <ceiling>
set -uo pipefail
res="$1"; out="$2"; label="$3"; sha="$4"; small="$5"; ctx="$6"; threads="$7"; ceiling="$8"; mkdir -p "$out"
apk=interface/labs/v3/app/build/outputs/apk/debug/app-debug.apk
tapk=interface/labs/v3/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
adb shell cmd connectivity airplane-mode enable || adb shell settings put global airplane_mode_on 1
adb shell settings get global airplane_mode_on | tee "$out/airplane.txt"; grep -qx 1 "$out/airplane.txt" || exit 1
adb install -r "$apk" && adb install -r -t "$tapk" || exit 1
for f in fr-bench-30.json fr-conv-01.json; do adb push "$res/$f" "/data/local/tmp/$f" >/dev/null; done
adb shell getprop ro.product.model > "$out/device.txt"; adb shell cat /proc/meminfo | head -3 >> "$out/device.txt"
adb push "$res/model.gguf" /data/local/tmp/study.gguf >/dev/null && adb shell chmod 644 /data/local/tmp/study.gguf
adb shell am instrument -w -r -e class fr.jarvis.v3.ModelStudyTest#benchOneModel -e model /data/local/tmp/study.gguf -e sha256 "$sha" \
  -e label "$label" -e small "$small" -e context "$ctx" -e threads "$threads" -e ceiling "$ceiling" \
  -e benches /data/local/tmp/fr-bench-30.json,/data/local/tmp/fr-conv-01.json fr.jarvis.v3.test/androidx.test.runner.AndroidJUnitRunner > "$out/instr-$label.txt" 2>&1
adb exec-out run-as fr.jarvis.v3 cat "files/study-$label.json" > "$out/study-$label.json" 2>/dev/null || rm -f "$out/study-$label.json"
adb shell rm -f /data/local/tmp/study.gguf /data/local/tmp/fr-bench-30.json /data/local/tmp/fr-conv-01.json
if grep -q '^OK (1 test)' "$out/instr-$label.txt"; then echo "PASS $label" | tee -a "$out/results.txt"; exit 0; fi
echo "FAIL $label" | tee -a "$out/results.txt"; tail -n 30 "$out/instr-$label.txt" | tee -a "$out/results.txt"; exit 1
