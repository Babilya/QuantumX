<button class="neon"><slot /></button>

<style>
.neon {
  background: linear-gradient(90deg,#FF1CC0,#1C3AFF);
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 10px;
  box-shadow: 0 0 10px #FF1CC0, 0 0 20px #1C3AFF;
  transition: transform .2s ease, box-shadow .2s ease;
}
.neon:hover { transform: translateY(-2px); box-shadow: 0 0 15px #FF1CC0, 0 0 30px #1C3AFF; }
</style>
