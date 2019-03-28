import { Router } from "express";
import BuildingController from "../controllers/BuildingController";

const router = Router();
router.get('/:id', BuildingController.getOneById);

export default router;