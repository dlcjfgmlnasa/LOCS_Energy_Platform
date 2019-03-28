import { Router } from "express";
import PowerController from "../controllers/PowerController";

const router = Router();
router.get('/:id', PowerController.getOneById);

export default router;