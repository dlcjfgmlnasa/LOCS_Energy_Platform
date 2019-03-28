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


@Entity()
export class Building extends BaseEntity{
  /* primary Key */
  @PrimaryGeneratedColumn() id: number;

  /* building comment (설명) */
  @Column({ type: "text" , nullable: true })
  comment: string;

  /* building latitude (위도) */
  @Column({ type: "double precision", default: 0 })
  lat: number;

  /* building longitude (경도) */
  @Column({ type: "double precision", default: 0 })
  lng: number;

  /* Power Info (전력 데이터 정보) */
  @OneToMany(type => Power, Power => Power.building)
  powers: Power[];

  @CreateDateColumn() createdAt: string;
  @UpdateDateColumn() updatedAt: string;

}