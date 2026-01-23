import os
import subprocess
import shutil

# --- 讀取分流設定 ---
def load_config():
    cfg = {
        'max_video_mb': 25.0, # 影片上限
        'max_image_mb': 5.0,  # 圖片上限，給予更嚴格的要求
        'target_width': 1280,
        'ffmpeg_bin': r'D:\Dropbox\Dependencies\ffmpeg.exe' # 妳的依賴路徑
    }
    if os.path.exists('setting.txt'):
        try:
            with open('setting.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    if ':' in line:
                        k, v = line.split(':', 1)
                        key = k.strip().lower()
                        if key in cfg: 
                            cfg[key] = float(v.strip().replace('mb','')) if 'mb' in key else v.strip()
                        elif key == 'ffmpeg_bin':
                            cfg['ffmpeg_bin'] = v.strip()
        except: pass
    return cfg

def shrink_media():
    cfg = load_config()
    ffmpeg = cfg['ffmpeg_bin']
    
    # 掃描當前資料夾
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    for f in files:
        name_root, ext = os.path.splitext(f)
        ext = ext.lower()
        size_mb = os.path.getsize(f) / (1024 * 1024)
        
        is_video = ext in ('.mp4', '.mov', '.avi')
        is_image = ext in ('.png', '.jpg', '.jpeg', '.webp', '.bmp')
        
        # 判定是否需要減肥
        should_shrink = False
        if is_video and size_mb > cfg['max_video_mb']:
            should_shrink = True
            target_ext = '.mp4'
            limit = cfg['max_video_mb']
        elif is_image and size_mb > cfg['max_image_mb']:
            should_shrink = True
            target_ext = '.webp'
            limit = cfg['max_image_mb']
            
        if should_shrink:
            print(f"🚨 抓到胖小孩: {f} ({size_mb:.2f}MB > {limit}MB)")
            temp_output = f"temp_shrink_{name_root}{target_ext}"
            
            if target_ext == '.mp4':
                # 影片：相容性優先 (H.264)
                cmd = [
                    ffmpeg, '-y', '-i', f,
                    '-vcodec', 'libx264', '-crf', '30', '-preset', 'slow',
                    '-vf', f"scale='min({cfg['target_width']},iw)':-2",
                    '-acodec', 'aac', '-b:a', '128k', temp_output
                ]
            else:
                # 圖片：WebP 高階壓縮
                cmd = [
                    ffmpeg, '-y', '-i', f,
                    '-vcodec', 'libwebp', '-compression_level', '6', 
                    '-q:v', '80', # 品質 80 是 WebP 的甜點位
                    '-vf', f"scale='min({cfg['target_width']},iw)':-2", temp_output
                ]
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                final_name = f"{name_root}{target_ext}"
                # 如果檔名變了 (例如 .png -> .webp)，刪除舊的
                if final_name != f:
                    os.remove(f)
                shutil.move(temp_output, final_name)
                print(f"✨ 減肥完成: {final_name} ({os.path.getsize(final_name)/1024/1024:.2f}MB)")
            except Exception as e:
                print(f"❌ 減肥失敗: {e}")
                if os.path.exists(temp_output): os.remove(temp_output)

if __name__ == "__main__":
    shrink_media()