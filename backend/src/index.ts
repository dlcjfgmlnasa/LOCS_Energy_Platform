import express from "express";
import dotenv from "dotenv";
import connectionOptions from "./ormConfig";
import { createConnection } from "typeorm";
dotenv.config();

const handleAppStart = () => console.log(`app listening on http://${process.env.HOST_DOMAIN}:${process.env.HOST_PORT}`);

createConnection(connectionOptions)
  .then(() => {
    // Create a new express application instance
    const app = express();
    app.listen(Number(process.env.HOST_PORT), String(process.env.HOST_DOMAIN), handleAppStart);
  })
  .catch(error => console.log(error));