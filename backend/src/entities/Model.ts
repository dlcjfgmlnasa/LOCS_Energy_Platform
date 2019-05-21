import {
    BaseEntity,
    Entity,
    Column,
    CreateDateColumn,
    ManyToOne,
    PrimaryGeneratedColumn,
    UpdateDateColumn
  } from "typeorm"
  import { Building } from "./Building";
  
  type MODEL_TYPE = "BROKEN" | "POWER";
  
  @Entity()
  export class Model extends BaseEntity{
    /* primary Key */
    @PrimaryGeneratedColumn("increment") id: number;
  
    /* 모델 종류 [Broken, Power] */
    @Column({ type: "enum", enum: ["BROKEN", "POWER"] })
    target: MODEL_TYPE;
  
    /* 모델 이름 (filepath) */
    @Column({ type: "varchar", length: 100 })
    filename: string;
  
    /* 모델 저장 위치 (filepath) */
    @Column({ type: "varchar", length: 200 })
    filepath: string;
  
    /* Building Info (빌딩 데이터 정보) */
    @ManyToOne(type => Building, Building => Building.models)
    building: Building;
  
    @CreateDateColumn() createdAt: string;
    @UpdateDateColumn() updatedAt: string;
  }
  
  export default Model;