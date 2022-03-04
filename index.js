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
		fname = file.fieldname + "-" + Date.now()+file.originalname;
	cb(null, file.fieldname + "-" + Date.now()+file.originalname)
	}
})
	
	
var upload_s = multer({
	storage: storage,
	fileFilter: function (req, file, cb){
	
		// Set the filetypes, it is optional
		var filetypes = /jpeg|jpg|png|pdf/;
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




app.get('/text', callName);

function callName(req, res) {
	
	// Use child_process.spawn method from	
	// child_process module and assign it
	// to variable spawn
	var spawn = require("child_process").spawn;
	
	// Parameters passed in spawn -
	// 1. type_of_script
	// 2. list containing Path of the script
	// and arguments for the script
	
	// E.g : http://localhost:3000/name?firstname=Mike&lastname=Will
	// so, first name = Mike and last name = Will


	// ffname = __dirname + "\\" + upload_folder + "\\" + fname


	console.log(fname);
	fname2 = fname.slice(0,-4);
	fname2 = fname2 + ".txt"
	var process1 = spawn('python',["./ocr2.py",
							fname] );
	// var process2 = spawn('python',["./parse_regex.py",
	// 						fname2] );

	// console.log(typeof(process));
	// Takes stdout data from script which executed
	// with arguments and send this data to res object

	// data1 = ""
	// data2 = ""
	process1.stdout.on('data', function(data) {
		// console.log(typeof(data.toString()));
		// const var1 = data.toString();
		// console.log(typeof(var1));
		// console.log(var1);
		// const obj = JSON.parse(data.toString());
		// console.log(obj);
		res.send(data.toString());
	} )
}


// Take any port number of your choice which
// is not taken by any other process

app.listen(process.env.PORT || 3000, function(){
    console.log("server is running @ 3000");

})
