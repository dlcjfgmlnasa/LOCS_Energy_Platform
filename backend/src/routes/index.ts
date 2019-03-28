import { Router } from "express";
import building from "./building";
import power from "./power";

const routes = Router();

routes.use('/building', building);
routes.use('/power', power);

export default routes;