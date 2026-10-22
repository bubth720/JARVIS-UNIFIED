"""Compile and execute generated Java and Kotlin DTOs against public examples.

Requires JDK17 (JAVA_HOME), plus kotlinc or KOTLIN_COMPILER_CLASSPATH and
KOTLIN_STDLIB. No downloads, Gradle, Android installation or production linkage.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from .generator import pascal
from .manifest import canonical, strict_json

ROOT = Path(__file__).resolve().parents[2]


def run(command):
    subprocess.run([str(x) for x in command], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated", type=Path, default=ROOT / "contracts/generated")
    args = parser.parse_args()
    jdk = Path(os.environ["JAVA_HOME"]) / "bin" if os.environ.get("JAVA_HOME") else None
    javac = str(jdk / "javac") if jdk else shutil.which("javac")
    java = str(jdk / "java") if jdk else shutil.which("java")
    if not javac or not java:
        raise SystemExit("JDK17 required: set JAVA_HOME. No tests were run.")
    examples = ROOT / "contracts/v1/examples"
    valid = sorted(examples.glob("*.valid.json"))
    with tempfile.TemporaryDirectory(prefix="jarvis-contracts-") as temp:
        directory = Path(temp)
        classes = directory / "classes"
        classes.mkdir()
        java_test = '''import java.nio.file.*;import java.util.*;import org.jarvis.contracts.v1.*;
public class ContractVectors {
static int checks=0;
static void expect(boolean ok){if(!ok)throw new AssertionError();checks++;}
static void reject(Runnable action){try{action.run();}catch(IllegalArgumentException e){checks++;return;}throw new AssertionError("invalid accepted");}
public static void main(String[] args)throws Exception{
'''
        kotlin_test = "import java.nio.file.*\nimport org.jarvis.contracts.v1.*\nfun main(args: Array<String>) {\n"
        for index, file in enumerate(valid):
            name = file.name.removesuffix(".valid.json")
            dto = pascal(name)
            canonical_file = directory / (name + ".canonical.json")
            canonical_file.write_bytes(canonical(strict_json(file.read_text(encoding="utf-8"))))
            java_test += f'String s{index}=Files.readString(Path.of(args[0],"{name}.valid.json"));\n'
            java_test += f'{dto} dto{index}={dto}.parse(s{index});\n'
            java_test += f'expect(dto{index}.toJson().equals(Files.readString(Path.of(args[1],"{name}.canonical.json"))));\n'
            java_test += f'expect({dto}.parseUtf8(Files.readAllBytes(Path.of(args[0],"{name}.valid.json"))).toMap().equals(dto{index}.toMap()));\n'
            java_test += f'reject(()->{dto}.parse(s{index}.replaceFirst("\\\\{{","{{\\\"unknown\\\":1,")));\n'
            java_test += f'reject(()->dto{index}.toMap().put("injected",true));\n'
            java_test += f'reject(()->{dto}.parse(FilesHelper.read(args[0],"{name}.invalid.json")));\n'
            kotlin_test += f'check({dto}Dto.parse(Files.readString(Path.of(args[0], "{name}.valid.json"))).toJson() == Files.readString(Path.of(args[1], "{name}.canonical.json")))\n'
        # Immutability throws UnsupportedOperationException (not IllegalArgumentException).
        java_test = java_test.replace('catch(IllegalArgumentException e)', 'catch(IllegalArgumentException|UnsupportedOperationException e)')
        java_test += '''
reject(()->ContractSupport.parse("{\\\"x\\\":1,\\\"x\\\":2}"));
reject(()->ContractSupport.parse("1.5"));reject(()->ContractSupport.parse("01"));
reject(()->ContractSupport.parse("NaN"));reject(()->ContractSupport.parse("true false"));
reject(()->ContractSupport.parse("\\\"\\\\ud800\\\""));
reject(()->ContractSupport.parseUtf8(new byte[]{(byte)0xc3,(byte)0x28}));
reject(()->ContractSupport.parse("[".repeat(66)+"0"+"]".repeat(66)));
reject(()->ContractSupport.parse(" ".repeat(65537)));
expect(ContractSupport.json(ContractSupport.parse("{\\\"😀\\\":1,\\\"z\\\":\\\"é\\\",\\\"\\ue000\\\":true}")).equals("{\\\"z\\\":\\\"é\\\",\\\"\\ue000\\\":true,\\\"😀\\\":1}"));
String request=Files.readString(Path.of(args[0],"request-envelope.valid.json"));
reject(()->RequestEnvelope.parse(request.replace("61000","1000")));
reject(()->RequestEnvelope.parse(request.replace("\\\"model_sha256\\\"","\\\"pack_sha256\\\"")));
String lease=Files.readString(Path.of(args[0],"resource-lease.valid.json"));
reject(()->ResourceLease.parse(lease.replace("\\\"stop_requested\\\"","\\\"released\\\"")));
Map<String,Object> req=RequestEnvelope.parse(request).toMap();
Map<String,Object> resp=ResponseEnvelope.parse(Files.readString(Path.of(args[0],"response-envelope.valid.json"))).toMap();
ContractSupport.validateExchange(req,resp);checks++;
Map<String,Object> stale=new LinkedHashMap<>(resp);stale.put("correlation_id","00000000-0000-4000-8000-000000000999");
reject(()->ContractSupport.validateExchange(req,stale));
System.out.println("Java contract checks="+checks);
}}
class FilesHelper{static String read(String dir,String file){try{return Files.readString(Path.of(dir,file));}catch(Exception e){throw new RuntimeException(e);}}}
'''
        kotlin_test += 'println("Kotlin round trips=5")\n}\n'
        (directory / "ContractVectors.java").write_text(java_test, encoding="utf-8")
        (directory / "ContractVectors.kt").write_text(kotlin_test, encoding="utf-8")
        run([javac, "-encoding", "UTF-8", "-d", classes, *sorted((args.generated / "java").rglob("*.java")), directory / "ContractVectors.java"])
        run([java, "-cp", classes, "ContractVectors", examples, directory])
        sources = sorted((args.generated / "kotlin").rglob("*.kt")) + [directory / "ContractVectors.kt"]
        stdlib = os.environ.get("KOTLIN_STDLIB")
        compiler = os.environ.get("KOTLIN_COMPILER_CLASSPATH")
        kotlinc = shutil.which("kotlinc")
        if compiler and stdlib:
            run([java, "-cp", compiler, "org.jetbrains.kotlin.cli.jvm.K2JVMCompiler", "-no-stdlib", "-no-reflect", "-jvm-target", "17", "-classpath", str(classes) + os.pathsep + stdlib, "-d", directory / "kotlin-classes", *sources])
            run([java, "-cp", os.pathsep.join([str(classes), str(directory / "kotlin-classes"), stdlib]), "ContractVectorsKt", examples, directory])
        elif kotlinc:
            run([kotlinc, "-jvm-target", "17", "-classpath", classes, "-include-runtime", "-d", directory / "kotlin.jar", *sources])
            run([java, "-cp", str(classes) + os.pathsep + str(directory / "kotlin.jar"), "ContractVectorsKt", examples, directory])
        else:
            raise SystemExit("Java verified; Kotlin NOT verified: configure kotlinc or KOTLIN_COMPILER_CLASSPATH/KOTLIN_STDLIB.")


if __name__ == "__main__":
    main()
