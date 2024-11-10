<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        table {
            margin: auto;
            width: 700px;
            border-radius: 5px;
            border-collapse: collapse;
            border-top: none;
        }
        input[type="text"] {
            border: 2px rgb(85, 86, 87) solid;
            width: 700px;
            height: 30px;
            border-radius: 5px;
            padding-left: 10px;
            font-size: 15px;
        }
        textarea {
            border: 2px (85, 86, 87) solid;
            width: 700px;
            height: 300px;
            border-radius: 5px;
            padding-left: 10px;
            font-size: 15px;
        }
        .header {
            height: 30px;
        }
        input[type="submit"] {
            width: 100px;
            height: 30px;
            border: 0;
            border-radius: 5px;
            background-color: rgb(85, 86, 87);
            color: rgb(255, 255, 255);
        }
        input[type="submit"]:active {
            width: 100px;
            height: 30px;
            border: 0;
            border-radius: 5px;
            background-color: rgb(85, 86, 87);
            color: rgb(255, 255, 255);
        }
        </style>
</head>
<body>
    <form action="/write" method="post" enctype="multipart/form-data">
        <table>
            <tr><td colspan="2"><h2>Write</h2></td></tr>
            <tr><td class="header">Title</td></tr>
            <tr><td><input type="text" name="title" placeholder="Title" /></td></tr>
            <tr><td class="header">Content</td></tr>
            <tr><td><textarea name="content" placeholder="Content" /></textarea></td></tr>
            <tr><td><button type="submit">Write</button></td></tr>
        </table>
    </form>

</body>
</html>