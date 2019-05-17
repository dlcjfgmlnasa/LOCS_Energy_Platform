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


@Entity()
export class Building extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn() id: number;

  /* building name (설명) */
  @Column({ type: "varchar" , nullable: true })
  name: string;

  /* building latitude (위도) */
  @Column({ type: "double precision", default: 0 })
  lat: number;

  /* building longitude (경도) */
  @Column({ type: "double precision", default: 0 })
  lng: number;

  /* bid */
  @Column({ type: "varchar", nullable: false, length: 6, unique: true})
  bld: string;

  /* Power Info (전력 데이터 정보) */
  @OneToMany(type => Power, Power => Power.building)
  powers: Power[];

  /* Broken Info (고장 데이터 정보) */
  @OneToMany(type => Broken, Broken => Broken.building)
  broken: Broken[];

  /* Model Info (모델 데이터 정보) */
  @OneToMany(type => Model, Model => Model.building)
  models: Model[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;
}

export default Building;