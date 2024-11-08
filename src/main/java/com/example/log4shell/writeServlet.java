package com.example.log4shell;

import java.io.*;
import javax.servlet.ServletException;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

//import com.sun.deploy.net.HttpRequest;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@WebServlet(name = "writeServlet", value = "/write")
public class writeServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {

        String title = req.getParameter("title");
        String content = req.getParameter("content");
        System.out.println("title : " + title);
        System.out.println("content : " + content);

        
        resp.setContentType("text/html");
        PrintWriter out = resp.getWriter();
        out.println("<html><body>");
        
        // vulnerable code
        Logger logger = LogManager.getLogger(com.example.log4shell.log4j.class);
        
        logger.error("Received request with title: " + title + " and content: " + content);
        out.println("<code> ! HI ! </u> </code>");
    }	

    public void destroy() {
    }
}

