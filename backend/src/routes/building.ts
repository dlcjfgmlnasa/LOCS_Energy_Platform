import { Router } from "express";
import BuildingController from "../controllers/BuildingController";

const router = Router();
const bldCnt = new BuildingController();

// 건물 리스트
router.get('/list', bldCnt.getBldList);
// 건물 상태 리스트
router.get('/list/status', bldCnt.getBldStatusList);

// 프로젝트 생성
router.post('/project', bldCnt.setNewProject);
// 프로젝트 상태 업데이트
router.post('/project/status', bldCnt.setStatus);

// 프로젝트 삭제
router.delete('/project', bldCnt.deleteProject);

export default router;