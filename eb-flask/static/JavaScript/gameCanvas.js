var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var gameBoard = new Image();
var BlackGamePiece = new Image();
var xpos;
var ypos;

gameBoard.onload = function () {
    ctx.drawImage(gameBoard, 0, 0, 480, 320);
};
gameBoard.src = '../static/JavaScript/GameElements/Connect4Board.png';

//BlackGamePiece.onload = function () {
//    ctx.drawImage(BlackGamePiece, 6, 0, 69, 69);
//};
//BlackGamePiece.src = '../static/JavaScript/GameElements/TitleTemplate.png';
//vertical
ctx.beginPath();
ctx.arc(240, 290, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(240, 240, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(240, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(240, 130, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(240, 80, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(240, 30, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "green";
ctx.fill();
ctx.closePath();
//horizontal
ctx.beginPath();
ctx.arc(442, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(374, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(306, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(174, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(106, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();

ctx.beginPath();
ctx.arc(39, 190, 28, 0, Math.PI * 2, false);
ctx.fillStyle = "blue";
ctx.fill();
ctx.closePath();
//tests
