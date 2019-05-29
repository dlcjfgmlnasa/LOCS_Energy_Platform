import {
  BaseEntity,
  Column,
  CreateDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  OneToMany,
  UpdateDateColumn
} from "typeorm";
import { Power } from "./Power";
import { Broken } from  "./Broken";
import { Model } from "./Model";

type PROJECT_STATUS = "PROCESSING" | "COMPLETE";

@Entity()
export class Building extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn() id: number;

  /* building name (건물 명) */
  @Column({ type: "varchar" , nullable: true })
  name: string;

   /* building name (설명) */
   @Column({ type: "varchar" , nullable: true })
   overview: string;

  /* learning status */
  @Column({ type: "enum", enum: ["PROCESSING", "COMPLETE"], default: "PROCESSING"})
  project_status: PROJECT_STATUS;

  /* Power Info (전력 데이터 정보) */
  @OneToMany(type => Power, Power => Power.building)
  powers: Power[];

  /* Broken Info (고장 데이터 정보) */
  @OneToMany(type => Broken, Broken => Broken.building)
  broken: Broken[];

  /* Model Info (모델 데이터 정보) */
  @OneToMany(type => Model, Model => Model.building,  { nullable: true })
  models: Model[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Building;