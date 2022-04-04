const express = require("express")
const path = require("path")
const multer = require("multer")
const { redirect } = require("express/lib/response")
const app = express()
	
// View Engine Setup
app.set("views",path.join(__dirname,"views"))
app.set("view engine","ejs")

var fname = "";
upload_folder = "uploads"
	
var storage = multer.diskStorage({
	destination: function (req, file, cb) {

		// Uploads is the Upload_folder_name
		cb(null, upload_folder)
	},
	filename: function (req, file, cb) {
		fname = file.fieldname + "-" + Date.now()+"-" +file.originalname;
	cb(null, file.fieldname + "-" + Date.now()+"-" +file.originalname)
	}
})
	
	
var upload_s = multer({
	storage: storage,
	fileFilter: function (req, file, cb){
	
		// Set the filetypes, it is optional
		var filetypes = /jpeg|jpg|png|pdf/;
		// var filetypes = /pdf/;

		var mimetype = filetypes.test(file.mimetype);

		var extname = filetypes.test(path.extname(
					file.originalname).toLowerCase());
		
		if (mimetype && extname) {
			return cb(null, true);
		}
	
		cb("Error: File upload only supports the "
				+ "following filetypes - " + filetypes);
	}

// mypic is the name of file attribute
}).single("mypic");	



app.get("/",function(req,res){
	res.render("Signup");
})
	
app.post("/upload/single",function (req, res, next) {
		
	// Error MiddleWare for multer file upload, so if any
	// error occurs, the image would not be uploaded!
	upload_s(req,res,function(err) {

		if(err) {

			// ERROR occured (here it can be occured due
			// to uploading image of size greater than
			// 1MB or uploading different file type)
			res.send(err)
		}
		else {

			// SUCCESS, image successfully uploaded
			// res.send("Success, Image uploaded!")
			res.redirect("/text")
		}
	})
})


function replaceAll(string, search, replace) {
    return string.split(search).join(replace);
  }


app.get('/text', callName);

function callName(req, res) {
	
	var spawn = require("child_process").spawn;

	console.log(fname);
	var process1 = spawn('python',["./ocr3.py",
							fname] );

	process1.stdout.on('data', function(data) {
		var x = data.toString()
		y = replaceAll(x, "'", '"')
		const obj = JSON.parse(y);
		console.log(obj);
		res.send(obj);
	} )
}


// Take any port number of your choice which
// is not taken by any other process

app.listen(process.env.PORT || 3000, function(){
    console.log("server is running @ 3000");

})
