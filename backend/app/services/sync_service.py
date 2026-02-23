from typing import Optional, Dict, Any, List
import asyncio
from app.services.pan115_service import pan115_service
from app.services.emby_service import emby_service
from app.utils.name_parser import name_parser

class SyncService:
    async def sync_tv_show(
        self,
        tmdb_id: int,
        share_url: str,
        target_folder_id: str,
        receive_code: str = ""
    ) -> Dict[str, Any]:
        """
        基于 Emby 查漏补缺的 115 转存策略
        """
        try:
            # 1. 查询 Emby 媒体库
            existing_episodes = await emby_service.get_downloaded_episodes(tmdb_id)
            print(f"Emby 中已存在的剧集 (TMDB ID: {tmdb_id}): {existing_episodes}")

            # 2 & 3. 解析 115 分享链接获取所有文件
            # 获取 share_code
            share_payload = None
            try:
                from p115client.util import share_extract_payload
                share_payload = share_extract_payload(share_url)
            except Exception:
                pass
                
            share_code = share_payload.get("share_code") if share_payload else pan115_service._extract_share_code(share_url)
            if not share_code:
                raise ValueError("无效的分享链接")

            if not receive_code:
                receive_code = share_payload.get("receive_code", "") if share_payload else ""

            # 递归获取分享链接内所有的文件
            all_files = await pan115_service.get_share_all_files_recursive(share_code, receive_code)
            if not all_files:
                return {"success": False, "message": "分享链接中没有找到文件", "saved_count": 0}

            missing_fids = []
            matched_files = []

            # 4. 文件名解析与过滤
            for f in all_files:
                filename = f.get("name", "")
                fid = f.get("fid")
                if not fid or not filename:
                    continue
                    
                # 尝试解析季号和集号
                parsed = name_parser.parse_episode(filename)
                
                # 如果无法解析出集号，为了保险起见，我们选择转存它，或者根据需求选择忽略。
                # 默认策略：如果解析成功且 Emby 中已存在，则跳过；否则转存。
                if parsed:
                    season, episode = parsed
                    if (season, episode) in existing_episodes:
                        print(f"跳过已存在剧集: {filename} (S{season:02d}E{episode:02d})")
                        continue
                else:
                    print(f"未能解析出集数的视频，默认加入转存队列: {filename}")
                
                missing_fids.append(str(fid))
                matched_files.append(filename)

            # 5. 精准转存
            if not missing_fids:
                return {"success": True, "message": "所有剧集均已存在，无需转存", "saved_count": 0}

            # 调用 115 API 批量转存
            # 注意: missing_fids 需要去重
            missing_fids = list(dict.fromkeys(missing_fids))
            print(f"准备转存 {len(missing_fids)} 个文件: {matched_files}")
            
            save_result = await pan115_service.save_share_files(
                share_code=share_code,
                file_ids=missing_fids,
                pid=target_folder_id,
                receive_code=receive_code
            )
            
            # 判断转存结果
            success = False
            if isinstance(save_result, dict):
                success = save_result.get("state", False) or save_result.get("success", False)

            if success:
                # 6. 触发 Emby 刷新 (不阻塞等待)
                asyncio.create_task(emby_service.refresh_library())
                return {
                    "success": True, 
                    "message": f"成功转存 {len(missing_fids)} 集", 
                    "saved_count": len(missing_fids),
                    "files": matched_files
                }
            else:
                return {
                    "success": False, 
                    "message": f"转存失败: {save_result}", 
                    "saved_count": 0
                }
                
        except Exception as e:
            return {"success": False, "message": f"同步过程中发生异常: {str(e)}", "saved_count": 0}

sync_service = SyncService()
