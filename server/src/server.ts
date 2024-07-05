import express from "express";
import morgan from "morgan";

const app = express();
const port = 6969;

app.use(morgan("tiny"));

app.get("/token", (req, res) => {
  res.send("token todo");
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
