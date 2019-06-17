import { Request, Response } from "express";
import { getRepository, getConnection } from "typeorm";
import { Building } from "../entities/Building";


/* Building Model (Build.ts) Controller */
class BuildingController {
  // 건물 리스트
  public getBldList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Building)
      .createQueryBuilder("building")
      .leftJoinAndSelect("building.models", "model")
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // 건물 리스트(상태)
  public getBldStatusList = async (req: Request, res: Response) => {
    try{
      const list = await getRepository(Building)
      .createQueryBuilder("building")
      .where("building.project_status = :project_status", { project_status: req.param('project_status') })
      .getMany();

      res.json(list);
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // 프로젝트 생성
  public setNewProject = async (req: Request, res: Response) => {
    try{
      await getConnection()
      .createQueryBuilder()
      .insert()
      .into(Building)
      .values({
        name: req.body.name,
        overview: req.body.overview
      })
      .execute();
      res.json({ status: 'ok' });
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

  // 프로젝트 삭제
  public deleteProject = async (req: Request, res: Response) => {
    try{
      await getConnection()
      .createQueryBuilder()
      .delete()
      .from(Building)
      .where("id = :id", { id: req.param('id') })
      .execute();
      res.json({ status: 'ok' });
    }
    catch(e){
      res.status(404).json({ message: e.message });
      throw new Error(e);
    }
  }

// 프로젝트 상태 변경
public setStatus = async (req: Request, res: Response) => {
  try{
    await getConnection()
    .createQueryBuilder()
    .update(Building)
    .set({ 
      project_status: req.body.project_status
    })
    .where("id = :id", { id: req.body.id })
    .execute();
    
    res.json({ status: 'ok' });    
  }
  catch(e){
    res.status(404).json({ message: e.message });
    throw new Error(e);
  }
}
}

export default BuildingController;