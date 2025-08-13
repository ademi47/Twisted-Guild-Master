from models import get_db_session, Guild, Member, Material, Contribution
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
import discord

class DatabaseManager:
    """Database operations manager for the Discord bot"""
    
    @staticmethod
    def ensure_guild_exists(guild_id: int, guild_name: str) -> None:
        """Ensure guild exists in database"""
        session = get_db_session()
        try:
            guild = session.query(Guild).filter(Guild.id == guild_id).first()
            if not guild:
                guild = Guild(id=guild_id, name=guild_name)
                session.add(guild)
                session.commit()
        finally:
            session.close()
    
    @staticmethod
    def ensure_member_exists(member_id: int, username: str, display_name: Optional[str] = None) -> None:
        """Ensure member exists in database"""
        session = get_db_session()
        try:
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                member = Member(
                    id=member_id,
                    username=username,
                    display_name=display_name or username
                )
                session.add(member)
                session.commit()
            else:
                # Update member info if changed
                current_display_name = display_name or username
                if member.username != username or member.display_name != current_display_name:
                    session.query(Member).filter(Member.id == member_id).update({
                        'username': username,
                        'display_name': current_display_name
                    })
                    session.commit()
        finally:
            session.close()
    
    @staticmethod
    def get_all_materials() -> List[Dict[str, Any]]:
        """Get all available materials"""
        session = get_db_session()
        try:
            materials = session.query(Material).order_by(Material.display_name).all()
            return [{"id": m.id, "name": m.name, "display_name": m.display_name, "value": m.value} for m in materials]
        finally:
            session.close()
    
    @staticmethod
    def get_material_by_name(material_name: str) -> Optional[Dict[str, Any]]:
        """Get material by name"""
        session = get_db_session()
        try:
            material = session.query(Material).filter(Material.name == material_name).first()
            if material:
                return {"id": material.id, "name": material.name, "display_name": material.display_name}
            return None
        finally:
            session.close()
    
    @staticmethod
    def add_contribution(guild_id: int, member_id: int, material_name: str, amount: int) -> bool:
        """Add a contribution record"""
        session = get_db_session()
        try:
            # Get material
            material = session.query(Material).filter(Material.name == material_name).first()
            if not material:
                return False
            
            # Create contribution
            contribution = Contribution(
                guild_id=guild_id,
                member_id=member_id,
                material_id=material.id,
                amount=amount
            )
            session.add(contribution)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error adding contribution: {e}")
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_member_contributions(guild_id: int, member_id: int) -> List[Dict[str, Any]]:
        """Get all contributions for a member in a guild"""
        session = get_db_session()
        try:
            contributions = session.query(
                Contribution, Material
            ).join(Material).filter(
                Contribution.guild_id == guild_id,
                Contribution.member_id == member_id
            ).all()
            
            result = []
            for contribution, material in contributions:
                result.append({
                    "material_name": material.display_name,
                    "amount": contribution.amount,
                    "created_at": contribution.created_at
                })
            return result
        finally:
            session.close()
    
    @staticmethod
    def get_guild_contributions_summary(guild_id: int) -> List[Dict[str, Any]]:
        """Get total contributions summary for a guild"""
        session = get_db_session()
        try:
            from sqlalchemy import func
            
            # Get total contributions per material
            results = session.query(
                Material.display_name,
                func.sum(Contribution.amount).label('total_amount'),
                func.count(Contribution.id).label('contribution_count')
            ).join(Contribution).filter(
                Contribution.guild_id == guild_id
            ).group_by(Material.id, Material.display_name).all()
            
            summary = []
            for display_name, total_amount, count in results:
                summary.append({
                    "material": display_name,
                    "total_amount": total_amount,
                    "contribution_count": count
                })
            
            return sorted(summary, key=lambda x: x['total_amount'], reverse=True)
        finally:
            session.close()
    
    @staticmethod
    def get_top_contributors(guild_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top contributors in a guild"""
        session = get_db_session()
        try:
            from sqlalchemy import func
            
            results = session.query(
                Member.display_name,
                Member.username,
                func.sum(Contribution.amount).label('total_contributions')
            ).join(Contribution).filter(
                Contribution.guild_id == guild_id
            ).group_by(Member.id, Member.display_name, Member.username).order_by(
                func.sum(Contribution.amount).desc()
            ).limit(limit).all()
            
            contributors = []
            for display_name, username, total in results:
                contributors.append({
                    "display_name": display_name,
                    "username": username,
                    "total_contributions": total
                })
            
            return contributors
        finally:
            session.close()
    
    @staticmethod
    def get_member_points(guild_id: int, member_id: int) -> float:
        """Calculate total contribution points for a member"""
        session = get_db_session()
        try:
            total_points = session.query(
                func.sum(Contribution.amount * Material.value).label('points')
            ).join(Material).filter(
                Contribution.guild_id == guild_id,
                Contribution.member_id == member_id
            ).scalar()
            
            return float(total_points or 0) / 100.0  # Convert back to decimal
        finally:
            session.close()
    
    @staticmethod
    def get_top_contributors_by_points(guild_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top contributors by points in a guild"""
        session = get_db_session()
        try:
            results = session.query(
                Member.display_name,
                Member.username,
                func.sum(Contribution.amount * Material.value).label('total_points')
            ).join(Contribution).join(Material).filter(
                Contribution.guild_id == guild_id
            ).group_by(Member.id, Member.display_name, Member.username).order_by(
                func.sum(Contribution.amount * Material.value).desc()
            ).limit(limit).all()
            
            contributors = []
            for display_name, username, total_points in results:
                contributors.append({
                    "display_name": display_name,
                    "username": username,
                    "total_points": float(total_points or 0) / 100.0  # Convert to decimal
                })
            
            return contributors
        finally:
            session.close()
    
    @staticmethod
    def get_member_contributions_with_points(guild_id: int, member_id: int) -> List[Dict[str, Any]]:
        """Get contributions with points calculation for a member"""
        session = get_db_session()
        try:
            contributions = session.query(
                Contribution, Material
            ).join(Material).filter(
                Contribution.guild_id == guild_id,
                Contribution.member_id == member_id
            ).all()
            
            result = []
            for contribution, material in contributions:
                points = float(int(contribution.amount) * material.value) / 100.0
                result.append({
                    "material_name": material.display_name,
                    "amount": contribution.amount,
                    "value_per_unit": float(material.value) / 100.0,
                    "points": points,
                    "created_at": contribution.created_at
                })
            return result
        finally:
            session.close()